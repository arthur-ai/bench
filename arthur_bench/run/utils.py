import json
import os
import getpass
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime

from arthur_bench import __version__
from arthur_bench.models.models import (
    TestCaseRequest,
    TestSuiteRequest,
    PaginatedTestSuite,
)
from arthur_bench.client.exceptions import UserValueError, ArthurInternalError
from arthur_bench.client.bench_client import BenchClient
from arthur_bench.scoring import ScoringMethod, scoring_method_class_from_string



def get_file_extension(filepath: Union[str, os.PathLike]) -> str:
    _, ext = os.path.splitext(filepath)
    return ext


def _initialize_metadata() -> Dict[str, Any]:
    return {
        "created_at": datetime.now().isoformat(),
        "bench_version": __version__,
        "created_by": getpass.getuser(),
    }

def _initialize_scoring_method(scoring_method_arg: Union[str, ScoringMethod], config: Optional[dict] = None) -> ScoringMethod:
    if isinstance(scoring_method_arg, str):
        scoring_method = scoring_method_class_from_string(scoring_method_arg)
        if config is not None:
            return scoring_method.from_dict(config)
        return scoring_method()
    else:
        return scoring_method_arg


def _validate_dataframe(data: pd.DataFrame, column: str):
    if column not in data.columns:
        raise UserValueError(f"column {column} not found in dataset")


def load_suite_from_dataframe(
    data: pd.DataFrame, input_column: str, reference_column: Optional[str] = None
) -> List[TestCaseRequest]:
    """
    Load test case data from a pandas dataframe.

    :param data: dataframe where each row is a test case consisting of a column for input and a column for reference
    :param input_column: column in dataframe containing inputs
    :param reference_column: column in dataframe containing reference outputs
    """
    _validate_dataframe(data, input_column)
    if reference_column is not None:
        _validate_dataframe(data, reference_column)
        suite = data.rename(
            columns={input_column: "input", reference_column: "reference_output"}
        )[["input", "reference_output"]]
    else:
        suite = data.rename(columns={input_column: "input"})[["input"]]
    if len(suite) < 1:
        raise UserValueError("test suite must have at least 1 test case")
    return [TestCaseRequest(**row) for row in suite.to_dict("records")]


def load_suite_from_csv(
    filepath: Union[str, os.PathLike],
    input_column: str,
    reference_column: Optional[str] = None,
) -> List[TestCaseRequest]:
    """
    Load test case data from csv file.

    :param filepath: string or pathlike object pointing to csv file
    :param input_column: column in file containing inputs
    :param reference_column: column in file containing reference outputs
    """
    if get_file_extension(filepath) != ".csv":
        raise UserValueError("filepath must be a csv file")
    return load_suite_from_dataframe(
        pd.read_csv(filepath), input_column, reference_column
    )


def load_suite_from_list(
    inputs: List[str], reference_outputs: Optional[List[str]]
) -> List[TestCaseRequest]:
    """
    Load test case data from lists of strings.

    :param inputs: list of string inputs for each test case
    :param reference_outputs: list of string reference outputs for each input
    """
    if len(inputs) < 1:
        raise UserValueError("test suite must have at least 1 test case")

    if reference_outputs is not None:
        if len(inputs) != len(reference_outputs):
            raise UserValueError("inputs and reference_outputs must be the same length")
        return [
            TestCaseRequest(input=i, reference_output=o)
            for i, o in zip(inputs, reference_outputs)
        ]

    return [TestCaseRequest(input=i, reference_output=None) for i in inputs]


def load_suite_from_json(filepath: Union[str, os.PathLike]) -> TestSuiteRequest:
    """
    Load a full test suite from a json file.

    :param filepath: string or pathlike object pointing to json file containing test suite data
    """
    if get_file_extension(filepath) != ".json":
        raise UserValueError("filepath must be json file")
    if isinstance(filepath, str):
        filepath = Path(filepath)
    return TestSuiteRequest.parse_file(filepath)  # type: ignore


def _load_suite_from_args(
    reference_data: Optional[pd.DataFrame] = None,
    reference_data_path: Optional[str] = None,
    input_column: str = "input",
    reference_column: Optional[str] = None,
    input_text_list: Optional[List[str]] = None,
    reference_output_list: Optional[List[str]] = None,
    requires_reference: bool = True,
) -> List[TestCaseRequest]:
    if requires_reference:
        if reference_column is None and reference_output_list is None:
            raise UserValueError(
                "scoring method requires reference data but no reference data was provided"
            )
    else:
        reference_column = None

    if reference_data is not None:
        return load_suite_from_dataframe(reference_data, input_column, reference_column)
    elif reference_data_path is not None:
        return load_suite_from_csv(reference_data_path, input_column, reference_column)
    elif input_text_list is not None:
        return load_suite_from_list(input_text_list, reference_output_list)
    else:
        raise UserValueError(
            "must specify data using either reference_data data frame, "
            "reference_data_path csv or input_text_list and reference_output_list strings"
        )


def _load_run_data_from_args(
    candidate_data: Optional[pd.DataFrame] = None,
    candidate_data_path: Optional[str] = None,
    candidate_column: str = "candidate_output",
    candidate_output_list: Optional[List[str]] = None,
    context_column: Optional[str] = None,
    context_list: Optional[List[str]] = None,
) -> Tuple[List[str], Optional[List[str]]]:
    if candidate_data is None and candidate_data_path is not None:
        if get_file_extension(candidate_data_path) != ".csv":
            raise UserValueError("filepath must be a csv file")
        candidate_data = pd.read_csv(candidate_data_path)

    if candidate_data is not None:
        _validate_dataframe(candidate_data, candidate_column)
        if context_column is not None:
            _validate_dataframe(candidate_data, context_column)
            return (
                candidate_data[candidate_column].values.tolist(),
                candidate_data[context_column].values.tolist(),
            )
        return candidate_data[candidate_column].values.tolist(), None

    elif candidate_output_list is not None:
        return candidate_output_list, context_list

    else:
        raise UserValueError(
            "must specify candidate data for run using candidate_data data frame, "
            "candidate_data_path csv, or candidate_output_list strings"
        )


def _get_suite_if_exists(
    client: BenchClient, name: str
) -> Optional[PaginatedTestSuite]:
    """
    TODO: add version validation
    """
    test_suite_resp = client.get_test_suites(name=name)
    if len(test_suite_resp.test_suites) > 0:
        # we enforce name validation, so there should ever only be one
        query_params = {"page_size": 100}
        suite = client.get_test_suite(
            str(test_suite_resp.test_suites[0].id), **query_params
        )
        current_page: int
        total_pages: int
        if suite.page is None or suite.total_pages is None:
            raise ArthurInternalError("expected paginated response")

        current_page = suite.page + 1
        total_pages = suite.total_pages
        while current_page <= total_pages:
            query_params["page"] = current_page
            suite_next_page = client.get_test_suite(
                str(test_suite_resp.test_suites[0].id), **query_params
            )
            suite.test_cases.extend(suite_next_page.test_cases)
            if suite_next_page.page is None or suite_next_page.total_pages is None:
                raise ArthurInternalError("expected paginated response")
            total_pages = suite_next_page.total_pages
            current_page = suite_next_page.page + 1
        return suite
    return None
