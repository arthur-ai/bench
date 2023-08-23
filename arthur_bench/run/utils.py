import pandas as pd
from typing import Optional, List, Tuple, Union

from arthur_bench.models.models import (
    TestCaseRequest,
)
from arthur_bench.exceptions import UserValueError
from arthur_bench.scoring import Scorer, scorer_from_string

from arthur_bench.utils.loaders import (
    load_suite_from_csv,
    load_suite_from_dataframe,
    load_suite_from_list,
    _validate_dataframe,
    get_file_extension,
)


def _initialize_scorer(
    scoring_method_arg: Union[str, Scorer], config: Optional[dict] = None
) -> Scorer:
    if isinstance(scoring_method_arg, str):
        scorer = scorer_from_string(scoring_method_arg)
        if config is not None:
            return scorer.from_dict(config)
        return scorer()
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
                "scoring method requires Reference Outputs but no "
                "Reference Output was provided. "
                "Please provide a reference_output_list or a reference_column"
                " name (if a DataFrame was used). "
                "View the Concepts Guide in the documentation for more info."
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
            "reference_data_path csv or input_text_list and reference_output_list "
            "strings"
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
