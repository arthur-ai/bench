import pytest
from arthur_bench.models.models import TestSuiteRequest, TestCaseRequest


@pytest.fixture(scope="session")
def mock_suite_cases():
    return [
        TestCaseRequest(
            input="this is test input to a language model",
            reference_output="this is test output from a language model",
        ),
        TestCaseRequest(
            input="this is another test prompt",
            reference_output="this is a test response",
        ),
    ]


@pytest.fixture(scope="session")
def mock_suite_cases_no_ref():
    return [
        TestCaseRequest(
            input="this is test input to a language model", reference_output=None
        ),
        TestCaseRequest(input="this is another test prompt", reference_output=None),
    ]


@pytest.fixture(scope="session")
def mock_suite_request(mock_suite_cases):
    return TestSuiteRequest(
        name="test_suite",
        description="my test suite",
        scoring_method="bertscore",
        created_at="2023-06-22T21:56:03.346141",
        created_by="arthur",
        bench_version="0.0.1",
        test_cases=mock_suite_cases,
    )


@pytest.fixture(scope="session")
def mock_suite_request_optional(mock_suite_cases_no_ref):
    return TestSuiteRequest(
        name="test_suite",
        scoring_method="bertscore",
        created_at="2023-06-22T21:56:03.346141",
        created_by="arthur",
        bench_version="0.0.1",
        test_cases=mock_suite_cases_no_ref,
    )


@pytest.fixture(scope="session")
def mock_suite_request_json():
    return '{"name": "test_suite", "description": "my test suite", "scoring_method": {"name": "bertscore", "type": "built_in"}, "test_cases": [{"input": "this is test input to a language model", "reference_output": "this is test output from a language model"}, {"input": "this is another test prompt", "reference_output": "this is a test response"}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141"}'


@pytest.fixture(scope="session")
def mock_suite_request_optional_json():
    return (
        '{"name": "test_suite", "description": null, "scoring_method": {"name": "bertscore", "type": "built_in"}, "test_cases": [{"input": "this is test input to a language model", "reference_output": null}, {"input": "this is another test prompt", "reference_output": null}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141"}'
        ""
    )
