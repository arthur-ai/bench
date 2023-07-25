import pytest
import pandas as pd
from unittest.mock import Mock, patch
from typing import List, Optional

from helpers import assert_test_suite_equal
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import ScoringMethod
from arthur_bench.scoring.summary_quality import SummaryQuality
from arthur_bench.run.testrun import TestRun


@pytest.fixture
def mock_openai_function_call():
    chain = Mock()
    chain.return_value = 0.0
    return chain


@pytest.fixture
def mock_summary_data():
    return pd.DataFrame(
        {
            'source': [
                'Breaking News: Earthquake measuring 7.2 magnitude strikes California. The earthquake originated near the city of Los Angeles and was felt across the region. Several buildings have collapsed, and there are reports of injuries and casualties. Rescue operations are underway.',
                'Just had the most amazing dinner at this new restaurant in town! The food was delicious, and the service was top-notch. I highly recommend it to everyone looking for a great dining experience.',
                'New study reveals the benefits of regular exercise. According to the research, engaging in physical activity for at least 30 minutes a day can significantly reduce the risk of heart disease, obesity, and other chronic conditions. Start incorporating exercise into your daily routine!',
                'Exciting announcement: The company is launching a new product next month. Stay tuned for more details and be among the first to experience this innovative offering.',
            ],
            'summary': [
                'A powerful earthquake hits California, causing damage and casualties.',
                'An enthusiastic review of a new restaurant in town with excellent food and service.',
                'Recent study highlights the positive impact of regular exercise on health.',
                'The company plans to release a new product, generating anticipation among customers.'
            ],
            'candidate_summary': [
                'Massive earthquake strikes California, causing destruction and loss of life.',
                'Had dinner at a new restaurant. Food and service were great!',
                'Exercise has health benefits and can reduce the risk of diseases.',
                'Exciting news: New product launch coming soon!'
            ]
        }
    )


# Test the run_batch method
def test_run_batch(mock_openai_function_call, mock_summary_data):
    with patch('arthur_bench.scoring.summary_quality.compare_summaries', return_value=mock_openai_function_call):

            # create summary quality scoring method
            summary_quality = SummaryQuality()

            # get run batch result
            result = summary_quality.run_batch(
                mock_summary_data['summary'],
                mock_summary_data['candidate_summary'],
                input_text_batch=mock_summary_data['source']
            )

            # assert LLMChain called with correct parameters
            for i in range(len(mock_summary_data)):
                mock_openai_function_call.assert_any_call(
                    mock_summary_data['source'][i],
                    mock_summary_data['summary'][i],
                    mock_summary_data['candidate_summary'][i])

            # assert correct return values for mock LLMChain outputs
            assert result == [0.0] * len(mock_summary_data)


