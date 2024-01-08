import pytest
from fastapi.testclient import TestClient

from arthur_bench.server.run_server import app
from arthur_bench.models.models import TestSuiteSortEnum
from tests.helpers import get_mock_client
from tests.fixtures.mock_responses import (
    MOCK_SUITES_JSON,
    MOCK_SUITE_RESPONSE_JSON,
    MOCK_RUNS_RESPONSE_JSON,
    MOCK_SUMMARY_RESPONSE_JSON,
    MOCK_RUN_RESPONSE_JSON,
)


@pytest.fixture
def mock_client():
    mock_arthur_client = get_mock_client(suite_exists=True)
    app.state.client = mock_arthur_client
    app.state.development = True  # disable telemetry during tests
    return TestClient(app)


TEST_SUITE_ID = "8b7ba080-8d14-42d2-9250-ec0edb96abd7"
RUN_ID = "af8466a8-6425-4ea5-85cb-ed952b26fa6c"


def test_get_test_suites(mock_client):
    resp = mock_client.get("/api/v3/bench/test_suites")
    assert resp.status_code == 200
    assert resp.json() == MOCK_SUITES_JSON


def test_get_test_suites_with_filters(mock_client):
    resp = mock_client.get(
        "/api/v3/bench/test_suites?scoring_method=bertscore&scoring_method=custom"
    )
    assert resp.status_code == 200
    assert resp.json() == MOCK_SUITES_JSON
    mock_client.app.state.client.get_test_suites.assert_called_once_with(
        page=1,
        page_size=5,
        sort=TestSuiteSortEnum.LAST_RUNTIME_ASC,
        scoring_method=["bertscore", "custom"],
        name=None,
    )


def test_get_test_suite_by_id(mock_client):
    resp = mock_client.get(f"/api/v3/bench/test_suites/{TEST_SUITE_ID}")
    assert resp.status_code == 200
    assert resp.json() == MOCK_SUITE_RESPONSE_JSON


def test_get_test_runs(mock_client):
    resp = mock_client.get(f"/api/v3/bench/test_suites/{TEST_SUITE_ID}/runs")
    assert resp.status_code == 200
    assert resp.json() == MOCK_RUNS_RESPONSE_JSON


def test_get_suite_summary(mock_client):
    resp = mock_client.get(f"/api/v3/bench/test_suites/{TEST_SUITE_ID}/runs/summary")
    assert resp.status_code == 200
    assert resp.json() == MOCK_SUMMARY_RESPONSE_JSON


def test_get_run(mock_client):
    resp = mock_client.get(f"/api/v3/bench/test_suites/{TEST_SUITE_ID}/runs/{RUN_ID}")
    assert resp.status_code == 200
    assert resp.json() == MOCK_RUN_RESPONSE_JSON
