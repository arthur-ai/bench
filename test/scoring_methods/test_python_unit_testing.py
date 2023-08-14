import pytest
from unittest.mock import Mock, patch, MagicMock, call

from arthur_bench.scoring.python_unit_testing import PythonUnitTesting
from fixtures.mock_data import MOCK_CODE_FAIL, MOCK_CODE_PASS, MOCK_CODE_EVAL_RESULT_FAIL, MOCK_CODE_EVAL_RESULT_PASS, \
    MOCK_UNIT_TEST_PASS, MOCK_UNIT_TEST_FAIL


@pytest.fixture
def mock_code_eval_success_and_failure():
    mock_eval = Mock()
    mock_eval.compute = Mock()
    mock_eval.compute.side_effect = [MOCK_CODE_EVAL_RESULT_PASS, MOCK_CODE_EVAL_RESULT_FAIL]
    return mock_eval


def test_run_batch(mock_code_eval_success_and_failure):
    with patch('arthur_bench.scoring.python_unit_testing.load', return_value=mock_code_eval_success_and_failure):
        unit_testing_scorer = PythonUnitTesting("test/fixtures/mock_python_unit_tests")
        result = unit_testing_scorer.run([MOCK_CODE_PASS, MOCK_CODE_FAIL])
        assert result == [1.0, 0.0]
        unit_testing_scorer.scorer.compute.assert_has_calls([
            call(references=[MOCK_UNIT_TEST_PASS], predictions=[[MOCK_CODE_PASS]]), 
            call(references=[MOCK_UNIT_TEST_FAIL], predictions=[[MOCK_CODE_FAIL]]
            )])
