import pytest
import shutil
from unittest import mock
from pathlib import Path
from arthur_bench.client.local import LocalBenchClient
from arthur_bench.client.local.client import _summarize_run
from arthur_bench.exceptions import UserValueError, NotFoundError
from arthur_bench.models.models import PaginatedTestSuite

from tests.fixtures.mock_responses import (
    MOCK_NO_SUITES,
    MOCK_SUITE_RESPONSE,
    MOCK_SUITE_CUSTOM_RESPONSE,
    MOCK_SUITES,
    MOCK_SUITES_CUSTOM_ONLY,
    MOCK_SUITES_ALL,
    MOCK_SUITE_RESPONSE_WITH_PAGES,
    MOCK_RUN_RESPONSE,
    MOCK_RUNS_RESPONSE,
    MOCK_SUMMARY,
    MOCK_SUMMARY_RESPONSE,
    MOCK_CATEGORICAL_RUN_RESPONSE,
    MOCK_CATEGORICAL_SUITE_RESPONSE,
    MOCK_CATEGORICAL_SUMMARY,
)
from tests.fixtures.mock_requests import MOCK_SUITE, MOCK_SUITE_CUSTOM, MOCK_RUN
from tests.helpers import assert_test_suite_equal

SUITE_NOT_FOUND = "72df9a40-1930-4d5e-ad62-31ca2c557079"
SUITE_EXISTS = "8b7ba080-8d14-42d2-9250-ec0edb96abd7"
RUN_EXISTS = "af8466a8-6425-4ea5-85cb-ed952b26fa6c"


def mock_summarize(run):
    return MOCK_SUMMARY


@pytest.fixture
def bench_temp_dir_empty(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp("bench"))
    yield tmpdir
    shutil.rmtree(str(tmpdir))


@pytest.fixture
def bench_temp_dir_with_suites(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp("bench"))
    shutil.copytree("tests/fixtures/mock_file_system", f"{tmpdir}/runs")
    yield f"{tmpdir}/runs"
    shutil.rmtree(str(tmpdir))


@pytest.fixture
def bench_temp_dir_with_runs(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp("bench"))
    shutil.copytree("tests/fixtures/mock_file_system_with_runs", f"{tmpdir}/runs")
    yield f"{tmpdir}/runs"
    shutil.rmtree(str(tmpdir))


def test_get_test_suites_empty(bench_temp_dir_empty):
    client = LocalBenchClient(bench_temp_dir_empty)
    suites = client.get_test_suites()
    assert suites == MOCK_NO_SUITES


def test_get_test_suite_empty(bench_temp_dir_empty):
    client = LocalBenchClient(bench_temp_dir_empty)
    with pytest.raises(NotFoundError):
        _ = client.get_test_suite(SUITE_NOT_FOUND)


@pytest.mark.parametrize(
    "req,expected_response",
    [
        (MOCK_SUITE_CUSTOM, MOCK_SUITE_CUSTOM_RESPONSE),
        (MOCK_SUITE, MOCK_SUITE_RESPONSE),
    ],
)
def test_create_test_suite(bench_temp_dir_empty, req, expected_response):
    client = LocalBenchClient(bench_temp_dir_empty)
    resp = client.create_test_suite(req)
    assert_test_suite_equal(resp, expected_response)

    bench_root = Path(bench_temp_dir_empty)
    assert (bench_root / req.name).is_dir()
    assert (bench_root / req.name / "run_id_to_name.json").is_file()
    expected_suite_file = bench_root / req.name / "suite.json"
    assert expected_suite_file.is_file()
    assert_test_suite_equal(
        PaginatedTestSuite.parse_file(expected_suite_file), expected_response
    )


def test_create_test_suite_exists(bench_temp_dir_with_suites):
    client = LocalBenchClient(bench_temp_dir_with_suites)
    with pytest.raises(expected_exception=UserValueError):
        _ = client.create_test_suite(MOCK_SUITE)


@pytest.mark.parametrize(
    "req, expected_response",
    [
        ({}, MOCK_SUITES_ALL),
        ({"name": "test_suite"}, MOCK_SUITES),
        ({"scoring_method": ["test_custom_scorer"]}, MOCK_SUITES_CUSTOM_ONLY),
        ({"name": "name doesn't exist"}, MOCK_NO_SUITES),
        ({"scoring_method": ["fake_scoring_method"]}, MOCK_NO_SUITES),
        ({"scoring_method": ["test_custom_scorer", "bertscore"]}, MOCK_SUITES_ALL),
    ],
    ids=[
        "no_params",
        "get_by_name",
        "get_by_scoring",
        "name_invalid",
        "scoring_invalid",
        "scoring_multiple",
    ],
)
def test_get_test_suites(bench_temp_dir_with_suites, req, expected_response):
    client = LocalBenchClient(bench_temp_dir_with_suites)
    resp = client.get_test_suites(**req)
    assert resp == expected_response


def test_get_test_suite_by_id(bench_temp_dir_with_suites):
    client = LocalBenchClient(bench_temp_dir_with_suites)
    resp = client.get_test_suite(SUITE_EXISTS)
    assert resp == MOCK_SUITE_RESPONSE_WITH_PAGES


def test_get_test_suite_by_id_not_found(bench_temp_dir_with_suites):
    client = LocalBenchClient(bench_temp_dir_with_suites)
    with pytest.raises(NotFoundError):
        _ = client.get_test_suite(SUITE_NOT_FOUND)


def test_get_suite_if_exists(bench_temp_dir_with_suites):
    client = LocalBenchClient(bench_temp_dir_with_suites)
    resp = client.get_suite_if_exists("test_suite")
    assert_test_suite_equal(resp, MOCK_SUITE_RESPONSE, check_page=False)


def test_get_suite_if_exists_not_found(bench_temp_dir_with_suites):
    client = LocalBenchClient(bench_temp_dir_with_suites)
    assert client.get_suite_if_exists("invalid name") == None


def test_create_test_run(bench_temp_dir_with_suites):
    client = LocalBenchClient(bench_temp_dir_with_suites)
    _ = client.create_new_test_run(SUITE_EXISTS, MOCK_RUN)

    bench_root = Path(bench_temp_dir_with_suites)
    assert (bench_root / "test_suite" / "test_run").is_dir()

    run_file = bench_root / "test_suite" / "test_run" / "run.json"
    assert run_file.is_file()

    suite = PaginatedTestSuite.parse_file((bench_root / "test_suite" / "suite.json"))
    assert suite.num_runs == 1
    assert suite.last_run_time is not None


def test_get_runs_for_suite(bench_temp_dir_with_runs):
    client = LocalBenchClient(bench_temp_dir_with_runs)
    resp = client.get_runs_for_test_suite(SUITE_EXISTS)
    assert resp == MOCK_RUNS_RESPONSE


def get_test_run(bench_temp_dir_with_runs):
    client = LocalBenchClient(bench_temp_dir_with_runs)
    resp = client.get_test_run(SUITE_EXISTS, RUN_EXISTS)
    assert resp == MOCK_RUN_RESPONSE


def create_test_run_suite_not_found(bench_temp_dir_with_runs):
    client = LocalBenchClient(bench_temp_dir_with_runs)
    with pytest.raises(NotFoundError):
        _ = client.create_new_test_run(SUITE_NOT_FOUND, MOCK_RUN)


def test_check_run_exists(bench_temp_dir_with_runs):
    client = LocalBenchClient(bench_temp_dir_with_runs)
    assert client.check_run_exists(SUITE_EXISTS, "test_run") == True
    assert client.check_run_exists(SUITE_EXISTS, "invalid run") == False


def get_summary_statistics(bench_temp_dir_with_runs):
    with mock.patch(
        "arthur_bench.client.local.client.LocalBenchClient._summarize_run",
        mock_summarize,
    ):
        client = LocalBenchClient(bench_temp_dir_with_runs)
        resp = client.get_summary_statistics(SUITE_EXISTS)
        assert resp == MOCK_SUMMARY_RESPONSE


@pytest.mark.parametrize(
    "run,scoring_config,expected",
    [
        (MOCK_RUN_RESPONSE, MOCK_SUITE_RESPONSE.scoring_method, MOCK_SUMMARY),
        (
            MOCK_CATEGORICAL_RUN_RESPONSE,
            MOCK_CATEGORICAL_SUITE_RESPONSE.scoring_method,
            MOCK_CATEGORICAL_SUMMARY,
        ),
    ],
)
def test_summarize_run(run, scoring_config, expected):
    summary = _summarize_run(run, scoring_config, num_bins=1)
    assert summary == expected
