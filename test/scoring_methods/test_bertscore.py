import pytest
from unittest.mock import Mock, MagicMock, patch
import torch

from arthur_bench.scoring.bertscore import BERTScore


@pytest.fixture
def mock_scorer():
    scorer = MagicMock()
    scorer.return_value.score.return_value = (
        torch.tensor([0.2, 0.4, 0.6, 0.8]),
        torch.tensor([0.1, 0.3, 0.5, 0.7]),
        torch.tensor([0.0, 0.2, 0.4, 0.6]),
    )
    return scorer


def test_run_bertscore(mock_summary_data, mock_scorer):
    with patch("arthur_bench.scoring.bertscore.BERTScorer", mock_scorer):
        bertscore = BERTScore()
        bertscore.load()

        bertscore_run_result = bertscore.run_batch(
            mock_summary_data["candidate_summary"],
            mock_summary_data["summary"],
        )

        # assert mock score called with correct values
        mock_scorer.return_value.score.assert_called_once_with(
            mock_summary_data["candidate_summary"],
            mock_summary_data["summary"],
            verbose=False,
        )

        # assert return correct values
        expected = [0.11, 0.31, 0.51, 0.71]
        for i, result in enumerate(bertscore_run_result):
            assert torch.isclose(
                torch.tensor(result), torch.tensor(expected[i]), atol=1e-5
            )
