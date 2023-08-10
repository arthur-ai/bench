import pytest
import pandas as pd
from unittest.mock import Mock, patch

from langchain.llms.fake import FakeListLLM
from arthur_bench.scoring.summary_quality import SummaryQuality


@pytest.fixture
def mock_llm():
    mock_llm = Mock()
    mock_llm.return_value = FakeListLLM
    return mock_llm


@pytest.fixture
def mock_llm_chain():
    chain = Mock()
    chain.return_value = {"text": "0"}
    return chain


# Test the run_batch method
def test_run_batch(mock_llm_chain, mock_llm, mock_summary_data):
    with patch('arthur_bench.scoring.summary_quality.LLMChain', return_value=mock_llm_chain):
        with patch('arthur_bench.scoring.summary_quality.ChatOpenAI', mock_llm):

            # create summary quality scoring method
            summary_quality = SummaryQuality()

            # get run batch result
            result = summary_quality.run_batch(
                mock_summary_data['candidate_summary'],
                mock_summary_data['summary'],
                input_text_batch=mock_summary_data['source']
            )

            # assert LLMChain called with correct parameters
            for i in range(len(mock_summary_data)):
                mock_llm_chain.assert_any_call({
                    "text": mock_summary_data['source'][i],
                    "summary_A": mock_summary_data['summary'][i],
                    "summary_B": mock_summary_data['candidate_summary'][i]})

            # assert correct return values for mock LLMChain outputs
            assert result == [0.0] * len(mock_summary_data)


# Test the run_batch method with different return values from LLMChain
@pytest.mark.parametrize('llm_return,expected', [
    ({"text": "0"}, [0.0]),
    ({"text": "1"}, [1.0]),
    ({"text": "tie"}, [0.5]),
    ({"text": "invalid"}, [-1.0]),
])
def test_run_batch_with_different_llm_returns(llm_return, expected, mock_llm_chain, mock_llm):
    mock_llm_chain.return_value = llm_return
    with patch('arthur_bench.scoring.summary_quality.LLMChain', return_value=mock_llm_chain):
        with patch('arthur_bench.scoring.summary_quality.ChatOpenAI', mock_llm):
            summary_quality = SummaryQuality()
            result = summary_quality.run_batch(["candidate"], ["reference"], ["input"])
            mock_llm_chain.assert_called_once_with({"text": "input", "summary_A": "reference", "summary_B": "candidate"})
            assert result == expected
