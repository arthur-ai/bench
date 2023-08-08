import pytest
import torch
import pandas as pd
from unittest.mock import Mock, MagicMock, patch

from arthur_bench.scoring.hedging_language import HedgingLanguage, DEFAULT_HEDGE

@pytest.fixture
def mock_scorer():
    scorer = MagicMock()
    scorer.return_value.score.return_value = (
        torch.tensor([0.4275, 0.4818, 0.4324]),
        torch.tensor([0.3951, 0.5723, 0.7113]),
        torch.tensor([0.4106, 0.4818, 0.5379]))
    return scorer

@pytest.fixture
def mock_hedging_langauge_data():
    return pd.DataFrame(
        {
            'instruction': [
                'How many teaspoons are in a tablespoon?',
                'Why are the Georgia Bulldogs back to back National Champions in Football?',
                'Who owns the best dog in the world?',
            ],
            'response': [
                'Three teaspoons are equivalent to one tablespoon.',
                'Coach Kirby Smart brought to Georgia what he learned as a longtime assistant with Nick Saban at Alabama and made his own process for Championship success. Smart has recruited the top high school players in the country to play for the Bulldogs and he has created a culture of brotherhood and accountability. The Georgia Bulldogs are now the standard of excellence when it comes to College Football.',
                'Reedo does because his little legend loves an away day and has great chat with the fam.',
            ],
            'candidate_output': [
                'There are 3 teaspoons in a tablespoon.',
                'As an AI, I provide real-time information up to October 2021. As of the last update, the Georgia Bulldogs are not back-to-back National Champions in Football. The team won its last National Championship in 1980. I recommend checking a recent sports news source to get the latest information.',
                'As an AI, I don\'t have personal opinions. However, "the best dog in the world" is subjective and can vary from person to person. It often refers to one\'s own pet, as the bond between a person and their pet is personal and unique. Thus, the owner of the "best dog in the world" could well be you or anyone who loves and cares for their dog deeply.',
            ],
        }
    )

def test_run_hedging_language(mock_hedging_langauge_data, mock_scorer):
    with patch('arthur_bench.scoring.hedging_language.BERTScorer', mock_scorer):

            hedging_language = HedgingLanguage()

            hedging_language_run_result = hedging_language.run_batch(
                candidate_batch=mock_hedging_langauge_data['candidate_output']
            )

            list_default_hedge = [DEFAULT_HEDGE] * len(mock_hedging_langauge_data['candidate_output'])

            # assert mock score called with correct values
            mock_scorer.return_value.score.assert_called_once_with(
                mock_hedging_langauge_data['candidate_output'], list_default_hedge, verbose=False
            )

            # assert return correct values
            expected = [0.0, 0.0, 1.0]
            for i, result in enumerate(hedging_language_run_result):
                assert torch.isclose(torch.tensor(result), torch.tensor(expected[i]), atol=1e-5)
