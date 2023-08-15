import pytest
from tests.fixtures.mock_requests import MOCK_RUN, MOCK_RUN_JSON


def test_run_serialization():
    assert MOCK_RUN.json() == MOCK_RUN_JSON
