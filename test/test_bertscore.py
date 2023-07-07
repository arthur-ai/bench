import pytest
import pandas as pd
from unittest.mock import Mock, patch
import torch
from typing import List, Optional

from langchain.llms.fake import FakeListLLM

from helpers import assert_test_suite_equal
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import ScoringMethod
from arthur_bench.scoring.bertscore import BERTScore, DEFAULT_MODEL, PRECISION_WEIGHT, RECALL_WEIGHT
from arthur_bench.run.testrun import TestRun

from test_summary_quality import mock_summary_data


@pytest.fixture
def mock_score():
    score = Mock()
    score.return_value = (
        torch.tensor([0.2, 0.4, 0.6, 0.8]),
        torch.tensor([0.1, 0.3, 0.5, 0.7]),
        torch.tensor([0.0, 0.2, 0.4, 0.6]))
    return score


def test_run_bertscore(mock_summary_data, mock_score):
    with patch('arthur_bench.scoring.bertscore.bert_score.score', mock_score):

            bertscore = BERTScore()

            bertscore_run_result = bertscore.run_batch(
                mock_summary_data['summary'],
                mock_summary_data['candidate_summary']
            )

            # assert mock score called with correct values
            mock_score.assert_called_once_with(
                mock_summary_data['candidate_summary'], mock_summary_data['summary'], lang='en',
                model_type=DEFAULT_MODEL, verbose=False
            )

            # assert return correct values
            expected = [.11, .31, .51, .71]
            for i, result in enumerate(bertscore_run_result):
                assert torch.isclose(torch.tensor(result), torch.tensor(expected[i]), atol=1e-5)



