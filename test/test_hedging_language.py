import pytest
import torch
from unittest.mock import MagicMock, patch
from fixtures.mock_data import MOCK_HEDGING_LANGUAGE

from arthur_bench.scoring.hedging_language import HedgingLanguage, DEFAULT_HEDGE


@pytest.fixture
def mock_scorer():
    scorer = MagicMock()
    scorer.return_value.score.return_value = (
        torch.tensor([0.4275, 0.4818, 0.4324]),
        torch.tensor([0.3951, 0.5723, 0.7113]),
        torch.tensor([0.4106, 0.4818, 0.5379]),
    )
    return scorer


def test_run_hedging_language(mock_scorer):
    with patch("arthur_bench.scoring.hedging_language.BERTScorer", mock_scorer):
        hedging_language = HedgingLanguage()

        hedging_language_run_result = hedging_language.run_batch(
            candidate_batch=MOCK_HEDGING_LANGUAGE["candidate_output"]
        )

        list_default_hedge = [DEFAULT_HEDGE] * len(
            MOCK_HEDGING_LANGUAGE["candidate_output"]
        )

        # assert mock score called with correct values
        mock_scorer.return_value.score.assert_called_once_with(
            MOCK_HEDGING_LANGUAGE["candidate_output"], list_default_hedge, verbose=False
        )

        # assert return correct values
        expected = [0.4106, 0.4818, 0.5379]
        for i, result in enumerate(hedging_language_run_result):
            assert torch.isclose(
                torch.tensor(result), torch.tensor(expected[i]), atol=1e-5
            )
