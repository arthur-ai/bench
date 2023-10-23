import pytest
from unittest.mock import Mock, MagicMock, patch
import torch


from tests.fixtures.mock_data import MOCK_SUMMARY_DATA
from arthur_bench.scoring.readability import Readability, max_flesch_reading_ease_value
from arthur_bench.scoring.word_count_match import WordCountMatch
from arthur_bench.scoring.specificity import Specificity
from textstat import flesch_reading_ease


@pytest.fixture
def mock_get_num_vague_words():
    mock = Mock()
    mock.score.return_value = 0.1
    return mock


@pytest.fixture
def mock_get_mean_word_freq():
    mock = Mock()
    mock.score.return_value = 0.2
    return mock


@pytest.fixture
def mock_get_pn_and_num():
    mock = Mock()
    mock.score.return_value = 0.3
    return mock


def test_run_readability():
    readability = Readability()

    readability_run_result = readability.run_batch(
        MOCK_SUMMARY_DATA["candidate_summary"], MOCK_SUMMARY_DATA["summary"]
    )

    # assert return correct values
    expected = [44.41, 91.27, 68.77, 64.37]
    for i, result in enumerate(readability_run_result):
        normalized_expected_result = expected[i] / max_flesch_reading_ease_value
        assert torch.isclose(
            torch.tensor(result),
            torch.tensor(normalized_expected_result),
            atol=1e-5,
        )


def test_run_wcm():
    word_count_match = WordCountMatch()

    wcm_run_result = word_count_match.run_batch(
        MOCK_SUMMARY_DATA["candidate_summary"], MOCK_SUMMARY_DATA["summary"]
    )

    # assert return correct values
    expected = [0.8888888, 0.7857142, 1.0, 0.583333]
    for i, result in enumerate(wcm_run_result):
        assert torch.isclose(torch.tensor(result), torch.tensor(expected[i]), atol=1e-5)


def test_specificity_mocks(
    mock_get_pn_and_num, mock_get_num_vague_words, mock_get_mean_word_freq
):
    with patch(
        "arthur_bench.scoring.specificity.Specificity.get_pn_and_num",
        mock_get_pn_and_num.score,
    ):
        with patch(
            "arthur_bench.scoring.specificity.Specificity.get_mean_word_freq",
            mock_get_mean_word_freq.score,
        ):
            with patch(
                "arthur_bench.scoring.specificity.Specificity.get_num_vague_words",
                mock_get_num_vague_words.score,
            ):
                specificity = Specificity()

                spec_run_result = specificity.run_batch(
                    MOCK_SUMMARY_DATA["candidate_summary"], MOCK_SUMMARY_DATA["summary"]
                )
                print("spec run:", spec_run_result)

                # assert mock functions called
                mock_get_pn_and_num.score.assert_called()
                mock_get_mean_word_freq.score.assert_called()
                mock_get_num_vague_words.score.assert_called()

                # assert return correct values
                expected = [0.198, 0.198, 0.198, 0.198]
                for i, result in enumerate(spec_run_result):
                    assert torch.isclose(
                        torch.tensor(result), torch.tensor(expected[i]), atol=1e-4
                    )


def test_specificity():
    specificity = Specificity()

    spec_run_result = specificity.run_batch(
        MOCK_SUMMARY_DATA["candidate_summary"], MOCK_SUMMARY_DATA["summary"]
    )

    # assert return correct values
    expected = [0.825000, 0.5829599, 0.5714, 0.895714]
    for i, result in enumerate(spec_run_result):
        assert torch.isclose(torch.tensor(result), torch.tensor(expected[i]), atol=1e-4)
