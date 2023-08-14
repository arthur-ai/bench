import pathlib
import uuid
from unittest.mock import Mock
from arthur_bench.models.models import (
    CreateRunRequest,
    PaginatedTestSuite,
    PaginatedTestSuites,
    PaginatedRuns,
    PaginatedRun,
    TestSuiteSummary,
)
from arthur_bench.client.bench_client import BenchClient
from fixtures.mock_responses import (
    MOCK_SUITE_RESPONSE,
    MOCK_NO_SUITES,
    MOCK_SUITES,
    MOCK_RUNS_RESPONSE,
    MOCK_SUITE_RESPONSE_WITH_PAGES,
    MOCK_SUMMARY_RESPONSE,
    MOCK_RUN_RESPONSE,
)

FIXTURE_FILE_DIR = pathlib.Path(__file__).parent / "fixtures"


# TODO: make generic equality checker minus id and created at fields


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


def assert_test_suites_equal(
    test_suites: PaginatedTestSuites, test_suites_other: PaginatedTestSuites
):
    assert len(test_suites.test_suites) == len(test_suites_other.test_suites)
    for i in range(len(test_suites.test_suites)):
        assert test_suites.test_suites[i].name == test_suites_other.test_suites[i].name
        assert (
            test_suites.test_suites[i].scoring_method
            == test_suites_other.test_suites[i].scoring_method
        )

    assert test_suites.page == test_suites_other.page
    assert test_suites.page_size == test_suites_other.page_size
    assert test_suites.total_count == test_suites_other.total_count
    assert test_suites.total_pages == test_suites_other.total_pages


def assert_test_run_equal(test_run: CreateRunRequest, test_run_other: CreateRunRequest):
    assert test_run.name == test_run_other.name
    assert test_run.test_cases == test_run_other.test_cases
    assert test_run.model_name == test_run_other.model_name
    assert test_run.model_version == test_run_other.model_version
    assert test_run.foundation_model == test_run_other.foundation_model


def assert_run_response_equal(run: PaginatedRun, run_other: PaginatedRun):
    assert len(run.test_cases) == len(run_other.test_cases)
    for i in range(len(run.test_run)):
        assert run.test_cases[i].input == run_other.test_cases[i].input
        assert (
            run.test_cases[i].reference_output
            == run_other.test_cases[i].reference_output
        )
        assert run.test_cases[i].output == run_other.test_cases[i].output
        assert run.test_cases[i].score == run_other.test_cases[i].score

    assert run.page == run_other.page
    assert run.page_size == run_other.page_size
    assert run.total_count == run_other.total_count
    assert run.total_pages == run_other.total_pages


def assert_runs_equal(run: PaginatedRuns, run_other: PaginatedRuns):
    assert len(run.test_runs) == len(run_other.test_runs)
    for i in range(len(run.test_runs)):
        assert run.test_runs[i].name == run_other.test_runs[i].name

    assert run.page == run_other.page
    assert run.page_size == run_other.page_size
    assert run.total_count == run_other.total_count
    assert run.total_pages == run_other.total_pages


def assert_summary_equal(summary: TestSuiteSummary, summary_other: TestSuiteSummary):
    assert len(summary.summary) == len(summary_other.summary)
    for i in range(len(summary.test_run)):
        assert summary.summary[i].name == summary_other.summary[i].name
        assert summary.summary[i].avg_score == summary_other.summary[i].avg_score
        assert summary.summary[i].histogram == summary_other.summary[i].histogram

    assert summary.page == summary_other.page
    assert summary.page_size == summary_other.page_size
    assert summary.total_count == summary_other.total_count
    assert summary.total_pages == summary_other.total_pages


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
