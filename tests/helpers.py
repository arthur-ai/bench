import pathlib
import uuid
from unittest.mock import Mock
from arthur_bench.models.models import PaginatedTestSuite, CreateRunRequest
from arthur_bench.client.bench_client import BenchClient
from tests.fixtures.mock_responses import (
    MOCK_SUITE_RESPONSE,
    MOCK_NO_SUITES,
    MOCK_SUITES,
    MOCK_RUNS_RESPONSE,
    MOCK_SUITE_RESPONSE_WITH_PAGES,
    MOCK_SUMMARY_RESPONSE,
    MOCK_RUN_RESPONSE,
)

FIXTURE_FILE_DIR = pathlib.Path(__file__).parent / "fixtures"


def assert_test_suite_equal(
    test_suite: PaginatedTestSuite,
    test_suite_other: PaginatedTestSuite,
    check_page=True,
):
    assert test_suite.name == test_suite_other.name
    assert test_suite.scoring_method == test_suite_other.scoring_method
    assert test_suite.description == test_suite_other.description
    assert len(test_suite.test_cases) == len(test_suite_other.test_cases)
    for i in range(len(test_suite.test_cases)):
        assert test_suite.test_cases[i].input == test_suite_other.test_cases[i].input
        assert (
            test_suite.test_cases[i].reference_output
            == test_suite_other.test_cases[i].reference_output
        )

    if check_page:
        assert test_suite.page == test_suite_other.page
        assert test_suite.page_size == test_suite_other.page_size
        assert test_suite.total_count == test_suite_other.total_count
        assert test_suite.total_pages == test_suite_other.total_pages


def assert_test_run_equal(test_run: CreateRunRequest, test_run_other: CreateRunRequest):
    assert test_run.name == test_run_other.name
    assert test_run.test_cases == test_run_other.test_cases
    assert test_run.model_name == test_run_other.model_name
    assert test_run.model_version == test_run_other.model_version
    assert test_run.foundation_model == test_run_other.foundation_model


def get_mock_client(suite_exists=False):
    client = Mock(spec=BenchClient)
    client.create_test_suite.return_value = MOCK_SUITE_RESPONSE
    client.create_new_test_run.return_value = uuid.uuid4()
    if not suite_exists:
        client.get_test_suites.return_value = MOCK_NO_SUITES
    else:
        client.get_test_suites.return_value = MOCK_SUITES
        client.get_test_suite.return_value = MOCK_SUITE_RESPONSE_WITH_PAGES
        client.get_runs_for_test_suite.return_value = MOCK_RUNS_RESPONSE
        client.get_summary_statistics.return_value = MOCK_SUMMARY_RESPONSE
        client.get_test_run.return_value = MOCK_RUN_RESPONSE
    return client
