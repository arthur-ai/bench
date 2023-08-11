import pytest
from unittest.mock import Mock, patch

from arthur_bench.scoring.hallucination import Hallucination

@pytest.fixture
def mock_hallucination_request():
    hallucination_request = Mock()
    hallucination_request.return_value = {"hallucination": "0", "reason": "this is the reason"}
    return hallucination_request

# Test the run_batch method
def test_run_batch(mock_hallucination_request, mock_summary_data):
    with patch('arthur_bench.scoring.hallucination.Hallucination.client.bench.score_hallucination', return_value=mock_hallucination_request):

        # create summary quality scoring method
        hallucination_score = Hallucination()

        # get run batch result
        result = hallucination_score.run_batch(
            mock_summary_data['candidate_summary'],
            mock_summary_data['source']
        )

        # assert LLMChain called with correct parameters
        for i in range(len(mock_summary_data)):
            mock_hallucination_request.assert_any_call({
                "response": mock_summary_data['candidate_summary'][i],
                "context": mock_summary_data['source'][i]})

        # assert correct return values for mock responses
        assert result == [0.0] * len(mock_summary_data)
