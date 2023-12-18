import os
import pytest
from unittest import mock
from unittest.mock import Mock, patch

from tests.fixtures.mock_data import MOCK_SUMMARY_DATA
from arthur_bench.scoring.summary_quality import (
    SummaryQuality,
    LLM_CHOICE_TO_CATEGORIES,
)
from arthur_bench.models.models import ScoreResult


@pytest.fixture
def mock_llm_chain():
    chain = Mock()
    chain.return_value = {"text": "0"}
    return chain


# Test the run_batch method
@mock.patch.dict(os.environ, {"OPENAI_API_KEY": "MOCK_API_KEY"})
def test_run_batch(mock_llm_chain):
    with patch(
        "arthur_bench.scoring.summary_quality.LLMChain", return_value=mock_llm_chain
    ):
        # create summary quality scoring method
        summary_quality = SummaryQuality()

        # get run batch result
        result = summary_quality.run_batch(
            MOCK_SUMMARY_DATA["candidate_summary"],
            MOCK_SUMMARY_DATA["summary"],
            input_text_batch=MOCK_SUMMARY_DATA["source"],
        )

        # assert LLMChain called with correct parameters
        for i in range(len(MOCK_SUMMARY_DATA)):
            mock_llm_chain.assert_any_call(
                {
                    "text": MOCK_SUMMARY_DATA["source"][i],
                    "summary_A": MOCK_SUMMARY_DATA["summary"][i],
                    "summary_B": MOCK_SUMMARY_DATA["candidate_summary"][i],
                }
            )

        # assert correct return values for mock LLMChain outputs
        assert result == [
            ScoreResult(score=0.0, category=LLM_CHOICE_TO_CATEGORIES["0"])
        ] * len(MOCK_SUMMARY_DATA)


# Test the run_batch method with different return values from LLMChain
@pytest.mark.parametrize(
    "llm_return,expected",
    [
        (
            {"text": "0"},
            [ScoreResult(score=0.0, category=LLM_CHOICE_TO_CATEGORIES["0"])],
        ),
        (
            {"text": "1"},
            [ScoreResult(score=1.0, category=LLM_CHOICE_TO_CATEGORIES["1"])],
        ),
        (
            {"text": "tie"},
            [ScoreResult(score=0.5, category=LLM_CHOICE_TO_CATEGORIES["tie"])],
        ),
        (
            {"text": "invalid"},
            [ScoreResult(score=-1.0, category=LLM_CHOICE_TO_CATEGORIES["default"])],
        ),
    ],
)
@mock.patch.dict(os.environ, {"OPENAI_API_KEY": "MOCK_API_KEY"})
def test_run_batch_with_different_llm_returns(llm_return, expected, mock_llm_chain):
    mock_llm_chain.return_value = llm_return
    with patch(
        "arthur_bench.scoring.summary_quality.LLMChain", return_value=mock_llm_chain
    ):
        summary_quality = SummaryQuality()
        result = summary_quality.run_batch(["candidate"], ["reference"], ["input"])
        mock_llm_chain.assert_called_once_with(
            {"text": "input", "summary_A": "reference", "summary_B": "candidate"}
        )
        assert result == expected
