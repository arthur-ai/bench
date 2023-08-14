import pytest
import pandas as pd
from helpers import FIXTURE_FILE_DIR
from fixtures.mock_responses import (
    MOCK_SUITE_RESPONSE,
    MOCK_SUITE_JSON,
    MOCK_SUITE_WITH_NULL,
    MOCK_SUITE_WITH_NULL_JSON,
    MOCK_SUITE_WITH_SCORING_CONFIG,
    MOCK_SUITE_WITH_SCORING_JSON,
)
from arthur_bench.run.utils import (
    load_suite_from_json,
    load_suite_from_dataframe,
    load_suite_from_list,
    load_suite_from_csv,
)


@pytest.mark.parametrize(
    "filepath, expected",
    [
        ("mock_suite.json", "mock_suite_request"),
        ("mock_suite_without_optional.json", "mock_suite_request_optional"),
        ("mock_suite_with_typed_score.json", "mock_suite_request_optional"),
        ("mock_suite_mixed_null_refs.json", ValueError),
    ],
)
def test_load_suite_from_json(filepath, expected, request):
    if isinstance(expected, str):
        assert load_suite_from_json(
            FIXTURE_FILE_DIR / filepath
        ) == request.getfixturevalue(expected)
    elif issubclass(expected, Exception):
        with pytest.raises(expected):
            load_suite_from_json(FIXTURE_FILE_DIR / filepath)
    else:
        raise RuntimeError("bad test structure")


def test_load_suite_from_csv(mock_suite_cases):
    assert (
        load_suite_from_csv(
            FIXTURE_FILE_DIR / "mock_suite.csv", "input", "reference_output"
        )
        == mock_suite_cases
    )


def test_load_suite_from_list(mock_suite_cases):
    inputs = ["this is test input to a language model", "this is another test prompt"]
    outputs = ["this is test output from a language model", "this is a test response"]
    assert load_suite_from_list(inputs, outputs) == mock_suite_cases


def test_load_suite_from_df(mock_suite_cases):
    df = pd.DataFrame(
        {
            "input": [
                "this is test input to a language model",
                "this is another test prompt",
            ],
            "reference_output": [
                "this is test output from a language model",
                "this is a test response",
            ],
        }
    )
    assert (
        load_suite_from_dataframe(df, "input", "reference_output") == mock_suite_cases
    )


@pytest.mark.parametrize(
    "object, expected",
    [
        (MOCK_SUITE_RESPONSE, MOCK_SUITE_JSON),
        (MOCK_SUITE_WITH_NULL, MOCK_SUITE_WITH_NULL_JSON),
        (MOCK_SUITE_WITH_SCORING_CONFIG, MOCK_SUITE_WITH_SCORING_JSON),
    ],
    ids=["base_suite", "suite_with_null", "suite_with_custom_scoring"],
)
def test_suite_serialization(object, expected):
    assert object.json() == expected
