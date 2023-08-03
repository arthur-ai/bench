import pathlib
import uuid
from unittest.mock import Mock
from arthur_bench.models.models import TestSuiteRequest
from arthur_bench.run.testrun import TestRun
from arthur_bench.client.bench_client import BenchClient
from fixtures.mock_responses import MOCK_SUITE, MOCK_NO_SUITES, MOCK_SUITES, MOCK_EXISTING_SUITE

FIXTURE_FILE_DIR = pathlib.Path(__file__).parent / "fixtures"


def assert_test_suite_equal(test_suite: TestSuiteRequest, test_suite_other: TestSuiteRequest):
    assert test_suite.name == test_suite_other.name
    assert test_suite.scoring_method == test_suite_other.scoring_method
    assert test_suite.description == test_suite_other.description
    assert test_suite.test_cases == test_suite_other.test_cases


def assert_test_run_equal(test_run: TestRun, test_run_other: TestRun):
    assert test_run.name == test_run_other.name
    assert test_run.test_case_outputs == test_run_other.test_case_outputs
    assert test_run.model_name == test_run_other.model_name
    assert test_run.model_version == test_run_other.model_version
    assert test_run.foundation_model == test_run_other.foundation_model


def get_mock_client(suite_exists=False):
    client = Mock(spec=BenchClient)
    client.create_test_suite.return_value = MOCK_SUITE
    client.create_new_test_run.return_value = uuid.uuid4()
    if not suite_exists:
        client.get_test_suites.return_value = MOCK_NO_SUITES
    else:
        client.get_test_suites.return_value = MOCK_SUITES
        client.get_test_suite.return_value = MOCK_EXISTING_SUITE
    return client