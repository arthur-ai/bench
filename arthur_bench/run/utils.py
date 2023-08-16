import getpass
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime

from arthur_bench import __version__
from arthur_bench.models.models import (
    TestCaseRequest,
    PaginatedTestSuite,
)
from arthur_bench.client.exceptions import UserValueError, ArthurInternalError
from arthur_bench.client.bench_client import BenchClient
from arthur_bench.scoring import ScoringMethod, scoring_method_class_from_string

from arthur_bench.utils.loaders import (
    load_suite_from_csv,
    load_suite_from_dataframe,
    load_suite_from_list,
    _validate_dataframe,
    get_file_extension,
)


def _initialize_metadata() -> Dict[str, Any]:
    return {
        "created_at": datetime.now().isoformat(),
        "bench_version": __version__,
        "created_by": getpass.getuser(),
    }


def _initialize_scoring_method(
    scoring_method_arg: Union[str, ScoringMethod], config: Optional[dict] = None
) -> ScoringMethod:
    if isinstance(scoring_method_arg, str):
        scoring_method = scoring_method_class_from_string(scoring_method_arg)
        if config is not None:
            return scoring_method.from_dict(config)
        return scoring_method()
    else:
        return scoring_method_arg


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
    Get a full test suite with name if it exists.

    :param client: BenchClient object for fetching test suite data
    :return: complete test suite with all test cases joined,
        or None if no suite with name exists
    :raises ArthurInternalError: if using a client that does not support pagination
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


def _check_run_exists(client: BenchClient, suite_id: str, run_name: str) -> bool:
    """
    Check if run with given name if it exists for suite with id suite_id

    :param client: BenchClient object for fetching test suite data
    :param suite_id: the id of the test suite to check run names
    :param run_name: the test run name to check for
    :return: True if run with name is found, False otherwise
    :raises ArthurInternalError: if using a client that does not support pagination
    """

    page_size = 100
    current_page = 1
    total_pages = 1
    page = 1

    while current_page <= total_pages:
        runs = client.get_runs_for_test_suite(suite_id, page=page, page_size=page_size)
        for run_metadata in runs.test_runs:
            if run_metadata.name == run_name:
                return True
        if runs.page is None or runs.total_pages is None:
            raise ArthurInternalError("expected paginated response")
        total_pages = runs.total_pages
        current_page = runs.page + 1
    return False
