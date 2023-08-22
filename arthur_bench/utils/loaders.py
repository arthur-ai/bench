import os
import pandas as pd
from pathlib import Path
from typing import Optional, List, Union

from arthur_bench.models.models import (
    TestCaseRequest,
    TestSuiteRequest,
)

from arthur_bench.exceptions import UserValueError


def get_file_extension(filepath: Union[str, os.PathLike]) -> str:
    _, ext = os.path.splitext(filepath)
    return ext


def _validate_dataframe(data: pd.DataFrame, column: str):
    if column not in data.columns:
        if column == "input":
            raise UserValueError(
                f"column: '{column}' not found in reference df. "
                "Creating TestSuite requires inputs. Specify input_"
                "column from reference df or provide input_text_list"
            )
        raise UserValueError(f"column: '{column}' not found in reference dataframe")


def load_suite_from_json(filepath: Union[str, os.PathLike]) -> TestSuiteRequest:
    """
    Load a full test suite from a json file.

    :param filepath: string or pathlike object pointing to json file containing test
        suite data
    """
    if get_file_extension(filepath) != ".json":
        raise UserValueError("filepath must be json file")
    if isinstance(filepath, str):
        filepath = Path(filepath)
    return TestSuiteRequest.parse_file(filepath)  # type: ignore


def load_suite_from_dataframe(
    data: pd.DataFrame, input_column: str, reference_column: Optional[str] = None
) -> List[TestCaseRequest]:
    """
    Load test case data from a pandas dataframe.

    :param data: dataframe where each row is a test case consisting of a column for i
        input and a column for reference
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
