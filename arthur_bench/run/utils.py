import json
import os
import getpass
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime

from arthur_bench import __version__
from arthur_bench.models.models import TestCaseRequest, TestSuiteRequest, ScoringMethod, TestSuiteResponse
from arthur_bench.client.exceptions import UserValueError

BENCH_FILE_DIR_KEY = 'BENCH_FILE_DIR'
DEFAULT_BENCH_FILE_DIR = Path(os.getcwd()) / "bench"


def get_file_extension(filepath: Union[str, os.PathLike]) -> str:
    _, ext = os.path.splitext(filepath)
    return ext


def _bench_root_dir() -> Path:
    return Path(os.environ.get(BENCH_FILE_DIR_KEY, DEFAULT_BENCH_FILE_DIR))


def _test_suite_dir(test_suite_name: str) -> Path:
    return Path(_bench_root_dir()) / test_suite_name


def _create_test_suite_dir(test_suite_name: str) -> Path:
    if not os.path.exists(_bench_root_dir()):
        os.mkdir(_bench_root_dir())
    test_suite_dir = _test_suite_dir(test_suite_name)
    if test_suite_dir.is_dir():
        raise UserValueError(f"test_suite {test_suite_name} already exists")
    os.mkdir(test_suite_dir)
    return test_suite_dir


def _initialize_metadata() -> Dict[str, Any]:
    return {
        "created_at": datetime.now().isoformat(),
        "bench_version": __version__,
        "created_by": getpass.getuser()
    }


def _create_run_dir(test_suite_name: str, run_name: str) -> Path:
    run_dir = _test_suite_dir(test_suite_name) / run_name 
    if os.path.exists(run_dir):
        raise UserValueError(f"run {run_name} already exists")
    os.mkdir(run_dir)
    return run_dir


def _clean_up_run(run_dir: Path):
    run_dir.rmdir()


def _validate_dataframe(data: pd.DataFrame, column: str):
    if column not in data.columns:
        raise UserValueError(f"column {column} not found in dataset")


def load_suite_from_dataframe(data: pd.DataFrame, input_column: str, reference_column: Optional[str] = None) -> List[TestCaseRequest]:
    """
    Load test case data from a pandas dataframe.

    :param data: dataframe where each row is a test case consisting of a column for input and a column for reference
    :param input_column: column in dataframe containing inputs
    :param reference_column: column in dataframe containing reference outputs
    """
    _validate_dataframe(data, input_column)
    if reference_column is not None:
        _validate_dataframe(data, reference_column)
        suite = data.rename(columns={input_column: "input", reference_column: "reference_output"})[["input", "reference_output"]]
    else:
        suite = data.rename(columns={input_column: "input"})[["input"]]
    if len(suite) < 1:
        raise UserValueError("test suite must have at least 1 test case")
    return [TestCaseRequest(**row) for row in suite.to_dict('records')]


def load_suite_from_csv(filepath: Union[str, os.PathLike], input_column: str, reference_column: Optional[str] = None) -> List[TestCaseRequest]:
    """
    Load test case data from csv file.

    :param filepath: string or pathlike object pointing to csv file
    :param input_column: column in file containing inputs
    :param reference_column: column in file containing reference outputs 
    """
    if get_file_extension(filepath) != '.csv':
        raise UserValueError("filepath must be a csv file")
    return load_suite_from_dataframe(pd.read_csv(filepath), input_column, reference_column)


def load_suite_from_list(inputs: List[str], reference_outputs: List[str]) -> List[TestCaseRequest]:
    """
    Load test case data from lists of strings.

    :param inputs: list of string inputs for each test case
    :param reference_outputs: list of string reference outputs for each input
    """
    if len(inputs) != len(reference_outputs):
        raise UserValueError("inputs and reference_outputs must be the same length")
    if len(inputs) < 1:
        raise UserValueError("test suite must have at least 1 test case")
    return [TestCaseRequest(input=i, reference_output=o) for i, o in zip(inputs, reference_outputs)]


def load_suite_from_json(filepath: Union[str, os.PathLike]) -> TestSuiteRequest:
    """
    Load a full test suite from a json file.

    :param filepath: string or pathlike object pointing to json file containing test suite data
    """
    if get_file_extension(filepath) != '.json':
        raise UserValueError("filepath must be json file")
    if isinstance(filepath, str):
        filepath = Path(filepath)
    return TestSuiteRequest.parse_file(filepath) # type: ignore


def _load_suite_from_args(
        reference_data: Optional[pd.DataFrame] = None,
        reference_data_path: Optional[str] = None,
        input_column: str = "input",
        reference_column: Optional[str] = None, 
        input_text_list: Optional[List[str]] = None,
        reference_output_list: Optional[List[str]] = None) -> List[TestCaseRequest]:
    if reference_data is not None:
        return load_suite_from_dataframe(reference_data, input_column, reference_column)
    elif reference_data_path is not None:
        return load_suite_from_csv(reference_data_path, input_column, reference_column)
    elif input_text_list is not None and reference_output_list is not None:
        return load_suite_from_list(input_text_list, reference_output_list)
    else:
        raise UserValueError("must specify data using either reference_data data frame, " 
                         "reference_data_path csv or input_text_list and reference_output_list strings")
    

def _load_run_data_from_args(
        candidate_data: Optional[pd.DataFrame] = None,
        candidate_data_path: Optional[str] = None,
        candidate_column: str = "candidate_output",
        candidate_output_list: Optional[List[str]] = None,
        context_column: Optional[str] = None,
        context_list: Optional[List[str]] = None) -> Tuple[List[str], Optional[List[str]]]:
    if candidate_data is None and candidate_data_path is not None:
        if get_file_extension(candidate_data_path) != '.csv':
            raise UserValueError("filepath must be a csv file")
        candidate_data = pd.read_csv(candidate_data_path)

    if candidate_data is not None:
        _validate_dataframe(candidate_data, candidate_column)
        if context_column is not None:
            _validate_dataframe(candidate_data, context_column)
            return candidate_data[candidate_column].values.tolist(), candidate_data[context_column].values.tolist()
        return candidate_data[candidate_column].values.tolist(), None
    
    elif candidate_output_list is not None:
        return candidate_output_list, context_list
    
    else:
        raise UserValueError("must specify candidate data for run using candidate_data data frame, "
                         "candidate_data_path csv, or candidate_output_list strings")


def _get_suite_if_exists(client, name: str) -> Optional[TestSuiteRequest]:
    """
    TODO: add version validation
    """
    test_suite_resp = client.get_test_suites(name=name)
    if len(test_suite_resp.test_suites) > 0:
        # we enforce name validation, so there should ever only be one
        return TestSuiteResponse(**test_suite_resp.test_suites[0].dict())
    return None

def _get_scoring_method(scoring_method: Union[str, ScoringMethod]) -> ScoringMethod:
    if isinstance(scoring_method, ScoringMethod):
        return scoring_method
    elif isinstance(scoring_method, str):
        try:
            return ScoringMethod(scoring_method)
        except ValueError:
            raise UserValueError(f"invalid scoring method: {scoring_method}")
    else:
        raise UserValueError(f"invalid scoring method: {scoring_method}")