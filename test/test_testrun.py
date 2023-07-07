import pytest

def test_run_serialization(mock_test_run, mock_test_run_json):
    assert mock_test_run.json(exclude={'test_suite_id', 'run_dir'}) == mock_test_run_json
