import pytest
import uuid
from http import HTTPStatus
from unittest import mock
from arthur_bench.client.http.requests import HTTPClient
from arthur_bench.client.rest.bench.client import ArthurBenchClient
from fixtures.mock_requests import (
    MOCK_SUITE,
    MOCK_SUITE_JSON,
    MOCK_RUN,
    MOCK_RUN_JSON_REST,
)


@pytest.fixture
def mock_http_client():
    mock_client = mock.MagicMock(spec=HTTPClient)
    return mock_client


@pytest.fixture
def mock_rest_client(mock_http_client):
    return ArthurBenchClient(http_client=mock_http_client)


def test_get_test_suites(mock_rest_client):
    with mock.patch("arthur_bench.client.rest.bench.client.PaginatedTestSuites"):
        _ = mock_rest_client.get_test_suites()
        mock_rest_client.http_client.get.assert_called_once_with(
            "/bench/test_suites",
            params={"page": 1, "page_size": 5},
            validation_response_code=HTTPStatus.OK,
        )


def test_get_test_suite_by_id(mock_rest_client):
    with mock.patch("arthur_bench.client.rest.bench.client.PaginatedTestSuite"):
        test_suite_id = uuid.uuid4()
        _ = mock_rest_client.get_test_suite(test_suite_id)
        mock_rest_client.http_client.get.assert_called_once_with(
            f"/bench/test_suites/{test_suite_id}",
            params={"page": 1, "page_size": 5},
            validation_response_code=HTTPStatus.OK,
        )


def test_create_test_suite(mock_rest_client):
    with mock.patch("arthur_bench.client.rest.bench.client.PaginatedTestSuite"):
        _ = mock_rest_client.create_test_suite(MOCK_SUITE)
        mock_rest_client.http_client.post.assert_called_once_with(
            "/bench/test_suites",
            json=MOCK_SUITE_JSON,
            validation_response_code=HTTPStatus.CREATED,
        )


def test_create_test_run(mock_rest_client):
    with mock.patch("arthur_bench.client.rest.bench.client.CreateRunResponse"):
        test_suite_id = uuid.uuid4()
        _ = mock_rest_client.create_new_test_run(test_suite_id, MOCK_RUN)
        mock_rest_client.http_client.post.assert_called_once_with(
            f"/bench/test_suites/{test_suite_id}/runs",
            json=MOCK_RUN_JSON_REST,
            validation_response_code=HTTPStatus.CREATED,
        )


def test_get_runs(mock_rest_client):
    with mock.patch("arthur_bench.client.rest.bench.client.PaginatedRuns"):
        test_suite_id = uuid.uuid4()
        _ = mock_rest_client.get_runs_for_test_suite(test_suite_id)
        mock_rest_client.http_client.get.assert_called_once_with(
            f"/bench/test_suites/{test_suite_id}/runs",
            params={"page": 1, "page_size": 5},
            validation_response_code=HTTPStatus.OK,
        )


def test_get_run_by_id(mock_rest_client):
    with mock.patch("arthur_bench.client.rest.bench.client.PaginatedRun"):
        test_suite_id = uuid.uuid4()
        test_run_id = uuid.uuid4()
        _ = mock_rest_client.get_test_run(test_suite_id, test_run_id)
        mock_rest_client.http_client.get.assert_called_once_with(
            f"/bench/test_suites/{test_suite_id}/runs/{test_run_id}",
            params={"page": 1, "page_size": 5},
            validation_response_code=HTTPStatus.OK,
        )


def test_get_summary(mock_rest_client):
    with mock.patch("arthur_bench.client.rest.bench.client.TestSuiteSummary"):
        test_suite_id = uuid.uuid4()
        _ = mock_rest_client.get_summary_statistics(test_suite_id)
        mock_rest_client.http_client.get.assert_called_once_with(
            f"/bench/test_suites/{test_suite_id}/runs/summary",
            params={"page": 1, "page_size": 5},
            validation_response_code=HTTPStatus.OK,
        )
