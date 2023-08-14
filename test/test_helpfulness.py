import pytest
from unittest.mock import Mock, MagicMock, patch
import torch

from arthur_bench.scoring.readability import Readability
from arthur_bench.scoring.word_count_match import WordCountMatch
from arthur_bench.scoring.specificity import Specificity
from textstat import flesch_reading_ease


def test_run_readability(mock_summary_data):

        readability = Readability()

        readability_run_result = readability.run_batch(
            mock_summary_data['candidate_summary'],
            mock_summary_data['summary']
        )

        # assert return correct values
        expected = [44.41, 91.27, 68.77, 64.37]
        for i, result in enumerate(readability_run_result):
            assert torch.isclose(torch.tensor(result), torch.tensor(expected[i]), atol=1e-5)


def test_run_wcm(mock_summary_data):

        word_count_match = WordCountMatch()

        wcm_run_result = word_count_match.run_batch(
            mock_summary_data['candidate_summary'],
            mock_summary_data['summary']
        )

        # assert return correct values
        expected = [0.8888888, 0.7857142, 1.0, 0.583333]
        for i, result in enumerate(wcm_run_result):
            assert torch.isclose(torch.tensor(result), torch.tensor(expected[i]), atol=1e-5)

def test_specificity(mock_summary_data):

        specificity = Specificity()

        spec_run_result = specificity.run_batch(
            mock_summary_data['candidate_summary'],
            mock_summary_data['summary']
        )

        #assert return correct values
        expected = [[0.825000, 0.5829599, 0.5714, 0.895714]]
        for i, result in enumerate(spec_run_result):
            assert torch.isclose(torch.tensor(result), torch.tensor(expected[i]), atol=1e-4)
