import pytest
import shutil
from arthur_bench.client.local import LocalBenchClient
from arthur_bench.client.exceptions import UserValueError, NotFoundError

from fixtures.mock_responses import (
    MOCK_NO_SUITES,
    MOCK_SUITE_RESPONSE,
    MOCK_SUITE_CUSTOM_RESPONSE,
    MOCK_SUITES,
    MOCK_SUITES_CUSTOM_ONLY,
    MOCK_SUITES_ALL,
    MOCK_SUITE_RESPONSE_WITH_PAGES,
    MOCK_RUNS_RESPONSE,
    MOCK_RUN_RESPONSE,
    MOCK_SUMMARY,
    MOCK_SUMMARY_RESPONSE,
)
from fixtures.mock_requests import MOCK_SUITE, MOCK_SUITE_CUSTOM, MOCK_RUN
from helpers import (
    assert_test_suite_equal,
    assert_test_suites_equal,
    assert_runs_equal,
    assert_run_response_equal,
    assert_summary_equal,
)

SUITE_NOT_FOUND = "72df9a40-1930-4d5e-ad62-31ca2c557079"

# TODO: these tests shouldn't depend on each other


def mock_summarize(run):
    return MOCK_SUMMARY


@pytest.fixture(scope="session")
def bench_temp_dir(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp("bench"))
    yield tmpdir
    shutil.rmtree(str(tmpdir))


@pytest.fixture(scope="session")
def local_client(bench_temp_dir):
    return LocalBenchClient(bench_temp_dir)


def test_get_test_suites_empty(local_client):
    suites = local_client.get_test_suites()
    assert suites == MOCK_NO_SUITES


@pytest.mark.parametrize(
    "req,expected_response",
    [
        (MOCK_SUITE_CUSTOM, MOCK_SUITE_CUSTOM_RESPONSE),
        (MOCK_SUITE, MOCK_SUITE_RESPONSE),
    ],
)
def test_create_test_suite(local_client, req, expected_response):
    resp = local_client.create_test_suite(req)
    assert_test_suite_equal(resp, expected_response)


def test_create_test_suite_exists(local_client):
    with pytest.raises(expected_exception=UserValueError):
        resp = local_client.create_test_suite(MOCK_SUITE)


@pytest.mark.parametrize(
    "req, expected_response",
    [
        ({}, MOCK_SUITES_ALL),
        ({"name": "test_suite"}, MOCK_SUITES),
        ({"scoring_method": "test_custom_scorer"}, MOCK_SUITES_CUSTOM_ONLY),
        ({"name": "name doesn't exist"}, MOCK_NO_SUITES),
        ({"scoring_method": "fake_scoring_method"}, MOCK_NO_SUITES),
    ],
    ids=[
        "no_params",
        "get_by_name",
        "get_by_scoring",
        "name_invalid",
        "scoring_invalid",
    ],
)
def test_get_test_suites(local_client, req, expected_response):
    resp = local_client.get_test_suites(**req)
    assert_test_suites_equal(resp, expected_response)


def test_get_test_suite_by_id(local_client):
    id_ = local_client.get_test_suites(name="test_suite").test_suites[0].id
    resp = local_client.get_test_suite(str(id_))
    assert_test_suite_equal(resp, MOCK_SUITE_RESPONSE_WITH_PAGES)


def test_get_test_suite_by_id_not_found(local_client):
    with pytest.raises(NotFoundError):
        _ = local_client.get_test_suite(SUITE_NOT_FOUND)


def test_create_test_run(local_client):
    id_ = local_client.get_test_suites(name="test_suite").test_suites[0].id
    _ = local_client.create_new_test_run(str(id_), MOCK_RUN)


def test_get_runs_for_suite(local_client):
    id_ = local_client.get_test_suites(name="test_suite").test_suites[0].id
    resp = local_client.get_runs_for_test_suite(str(id_))
    assert_runs_equal(resp, MOCK_RUNS_RESPONSE)


def get_test_run(local_client):
    id_ = local_client.get_test_suites(name="test_suite").test_suites[0].id
    runs = local_client.get_runs_for_test_suite(str(id_))
    resp = local_client.get_test_run(str(id_), str(runs.test_runs[0].id))
    assert_run_response_equal(resp, MOCK_RUN_RESPONSE)


def get_summary_statistics(local_client):
    id_ = local_client.get_test_suites(name="test_suite").test_suites[0].id
    resp = local_client.get_summary_statistics(str(id_))
    assert_summary_equal(resp, MOCK_SUMMARY_RESPONSE)
