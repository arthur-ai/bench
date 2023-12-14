from collections import defaultdict
import pytest
import pandas as pd
from unittest import mock
from typing import List, Optional

from tests.helpers import (
    assert_test_suite_equal,
    assert_test_run_equal,
    get_mock_client,
)
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import Scorer
from tests.fixtures.mock_requests import MOCK_SUITE, MOCK_SUITE_CUSTOM, MOCK_RUN
from tests.fixtures.mock_responses import (
    MOCK_SUITE_RESPONSE_WITH_PAGES,
    MOCK_SUITE_CUSTOM_RESPONSE_WITH_PAGES,
)
from tests.fixtures.mock_data import (
    MOCK_DATAFRAME,
    MOCK_INPUTS,
    MOCK_REFERENCE_OUTPUTS,
    MOCK_CUSTOM_DATAFRAME,
    MOCK_OUTPUTS,
)


@pytest.fixture
def mock_client():
    return get_mock_client()


@pytest.fixture
def test_suite_default(mock_load_scoring, mock_client):
    with mock.patch("arthur_bench.run.testsuite._initialize_scorer", mock_load_scoring):
        return TestSuite(
            name="test_suite",
            scoring_method="bertscore",
            reference_data=MOCK_DATAFRAME,
            client=mock_client,
        )


class MockScoringMethod(Scorer):
    @staticmethod
    def name():
        return "bertscore"

    @staticmethod
    def type():
        return "built_in"

    def run_batch(
        self,
        reference_batch: List[str],
        candidate_batch: List[str],
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[float]:
        return [0.9, 0.7]


class CustomScorer(Scorer):
    def __init__(self, custom_name="param_name"):
        self.custom_name = custom_name

    @staticmethod
    def name():
        return "test_custom_scorer"

    def run_batch(
        self,
        reference_batch: List[str],
        candidate_batch: List[str],
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[float]:
        return [0.5 for _ in range(len(reference_batch))]


@pytest.fixture(scope="session")
def mock_load_scoring():
    def load_scoring_method(scoring_method_arg):
        return MockScoringMethod()

    return load_scoring_method


@pytest.mark.parametrize(
    "params,expected",
    [
        (
            {
                "name": "test_suite",
                "scoring_method": "bertscore",
                "reference_data": MOCK_DATAFRAME,
            },
            MOCK_SUITE,
        ),
        (
            {
                "name": "test_suite_custom",
                "scoring_method": CustomScorer(),
                "description": "test_description",
                "reference_data": MOCK_CUSTOM_DATAFRAME,
                "input_column": "custom_prompt",
                "reference_column": "custom_reference",
            },
            MOCK_SUITE_CUSTOM,
        ),
        (
            {
                "name": "test_suite",
                "scoring_method": "bertscore",
                "input_text_list": MOCK_INPUTS,
                "reference_output_list": MOCK_REFERENCE_OUTPUTS,
            },
            MOCK_SUITE,
        ),
    ],
    ids=[
        "test-suite-default-columns",
        "test-suite-custom-columns",
        "test-suite-string-no-context",
    ],
)
def test_create_test_suite(params, expected, mock_client):
    suite = TestSuite(client=mock_client, **params)
    suite.client.get_suite_if_exists.assert_called_once_with(name=params["name"])
    suite.client.create_test_suite.assert_called_once()
    _, args, _ = suite.client.create_test_suite.mock_calls[0]
    assert_test_suite_equal(args[0], expected, check_page=False)


@pytest.mark.parametrize(
    "params,found_model",
    [
        (
            {"name": "test_suite", "scoring_method": "bertscore"},
            MOCK_SUITE_RESPONSE_WITH_PAGES,
        ),
        (
            {"name": "test_suite_custom", "scoring_method": CustomScorer()},
            MOCK_SUITE_CUSTOM_RESPONSE_WITH_PAGES,
        ),
    ],
    ids=["valid_builtin", "valid_custom"],
)
def test_reload_test_suite(params, found_model):
    mock_client = get_mock_client(suite_exists=True, mock_suite=found_model)
    suite = TestSuite(client=mock_client, **params)
    suite.client.get_suite_if_exists.assert_called_once_with(name=params["name"])
    suite.client.create_test_suite.assert_not_called()
    assert_test_suite_equal(suite._data, found_model)
    assert suite.scorer is not None


@pytest.mark.parametrize("candidate_column", ["custom_candidate", None])
def test_run_test_suite(candidate_column, test_suite_default):
    if candidate_column:
        run = test_suite_default.run(
            run_name="test_run",
            candidate_data=pd.DataFrame({candidate_column: MOCK_OUTPUTS}),
            candidate_column=candidate_column,
            model_name="my_very_special_gpt",
            save=False,
            batch_size=2,
        )
    else:
        run = test_suite_default.run(
            run_name="test_run",
            candidate_data=pd.DataFrame({"candidate_output": MOCK_OUTPUTS}),
            model_name="my_very_special_gpt",
            save=False,
            batch_size=2,
        )

    assert_test_run_equal(run, MOCK_RUN)


@pytest.mark.parametrize(
    "params",
    [
        {},
        {
            "input_column": "missing_prompt",
            "reference_data": pd.DataFrame({"prompt": [], "reference": []}),
        },
        {
            "reference_column": "missing_reference",
            "reference_data": pd.DataFrame({"prompt": [], "reference": []}),
        },
    ],
    ids=["missing-req-params", "input-missing", "reference-missing"],
)
def test_create_test_suite_invalid(params, mock_client):
    params.update({"name": "test_suite", "scoring_method": "bertscore"})
    with pytest.raises(ValueError):
        _ = TestSuite(client=mock_client, **params)


@pytest.mark.parametrize(
    "params",
    [
        {
            "candidate_column": "missing_candidate",
            "candidate_data": pd.DataFrame(
                {"candidate_output": ["three", "outputs", "provided"]}
            ),
        },
        {"candidate_data": pd.DataFrame({"candidate_output": ["only one output"]})},
    ],
    ids=["missing-candidate", "invalid-length"],
)
def test_run_test_suite_invalid(params, test_suite_default):
    params.update({"run_name": "test_run"})
    with pytest.raises(ValueError):
        _ = test_suite_default.run(**params)
