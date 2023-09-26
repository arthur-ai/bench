import pytest
from unittest.mock import Mock, patch

from tests.helpers import get_mock_client
from arthur_bench.scoring.hallucination import Hallucination
from arthur_bench.models.scoring import HallucinationScoreResponse
from tests.fixtures.mock_data import MOCK_SUMMARY_DATA


@pytest.fixture
def mock_client():
    mock_client = get_mock_client()
    mock_client.bench = Mock()
    mock_client.bench.score_hallucination = Mock()
    mock_client.bench.score_hallucination.return_value = HallucinationScoreResponse(
        hallucination=False, reason="Nothing wrong caught by the hallucination detector"
    )
    return mock_client


# Test the run_batch method
def test_run_batch(mock_client):
    with patch(
        "arthur_bench.scoring.hallucination.ArthurClient", return_value=mock_client
    ):
        # create summary quality scoring method (with a mocked client)
        hallucination_score = Hallucination()

        # get run batch result from mock client call
        result = hallucination_score.run_batch(
            MOCK_SUMMARY_DATA["candidate_summary"],
            input_text_batch=MOCK_SUMMARY_DATA["input_text"],
            context_batch=MOCK_SUMMARY_DATA["source"],
        )

        # assert mock score_hallucination called with correct parameters
        for i in range(len(MOCK_SUMMARY_DATA)):
            hallucination_score.client.bench.score_hallucination.assert_any_call(
                {
                    "user_input": MOCK_SUMMARY_DATA["input_text"][i],
                    "context": MOCK_SUMMARY_DATA["source"][i],
                    "response": MOCK_SUMMARY_DATA["candidate_summary"][i],
                }
            )

        # assert correct return values for mock responses
        assert result == [1.0] * len(MOCK_SUMMARY_DATA)
