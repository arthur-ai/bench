import pytest
from unittest.mock import Mock, MagicMock, patch
import torch

from arthur_bench.scoring.readability import Readability
from arthur_bench.scoring.word_count_match import WordCountMatch
from arthur_bench.scoring.specificity import Specificity
from textstat import flesch_reading_ease

@pytest.fixture
def mock_get_num_vague_words():
    scorer = MagicMock()
    scorer.return_value = (1)
    return scorer

@pytest.fixture
def mock_get_mean_word_freq():
    scorer = MagicMock()
    scorer.return_value = (0.0004)
    return scorer

@pytest.fixture
def mock_get_pn_and_num():
    scorer = MagicMock()
    scorer.return_value = (2)
    return scorer

@pytest.fixture
def mock_lexicon_count():
    scorer = MagicMock()
    scorer.return_value = (10)
    return scorer


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
    with (
        patch('arthur_bench.scoring.specificity.Specificity.get_num_vague_words') as mock_get_num_vague_words,
        patch('arthur_bench.scoring.specificity.Specificity.get_mean_word_freq') as mock_get_mean_word_freq,
        patch('arthur_bench.scoring.specificity.Specificity.get_pn_and_num') as mock_get_pn_and_num,
        patch('arthur_bench.scoring.specificity.lexicon_count') as mock_lexicon_count
    )

        specificity = Specificity()

        spec_run_result = specificity.run_batch(
            mock_summary_data['candidate_summary'],
            mock_summary_data['summary']
        )

        #assert mock functions called 
        mock_get_num_vague_words.assert_called_with(mock_summary_data['candidate_summary'][-1])
        mock_get_mean_word_freq.assert_called_with(mock_summary_data['candidate_summary'][-1])
        mock_get_pn_and_num.assert_called_with(mock_summary_data['candidate_summary'][-1])
        mock_lexicon_count.assert_called_with(mock_summary_data['candidate_summary'][-1])

        #assert return correct values
        expected = [0.8250, 0.8250, 0.8250, 0.8250]
        for i, result in enumerate(spec_run_result):
            assert torch.isclose(torch.tensor(result), torch.tensor(expected[i]), atol=1e-4)
