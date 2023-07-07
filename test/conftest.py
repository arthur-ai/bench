import pytest
from arthur_bench.models.models import TestSuiteRequest, TestCaseRequest, TestCaseOutput
from arthur_bench.run.testrun import TestRun


@pytest.fixture(scope='session')
def mock_suite_cases():
    return [
            TestCaseRequest(input="this is test input to a language model",
                            reference_output="this is test output from a language model"),
            TestCaseRequest(input="this is another test prompt",
                            reference_output="this is a test response")
        ]


@pytest.fixture(scope='session')
def mock_suite_request(mock_suite_cases):
    return TestSuiteRequest(
        name="test_suite",
        description="my test suite",
        scoring_method="bertscore",
        created_at="2023-06-22T21:56:03.346141",
        created_by="arthur",
        bench_version="0.0.1",
        test_cases=mock_suite_cases
    )

@pytest.fixture(scope='session')
def mock_suite_request_optional(mock_suite_cases):
    return TestSuiteRequest(
        name="test_suite",
        scoring_method="bertscore",
        created_at="2023-06-22T21:56:03.346141",
        created_by="arthur",
        bench_version="0.0.1",
        test_cases=mock_suite_cases
    )

@pytest.fixture(scope='session')
def mock_suite_request_json():
    return '{"name": "test_suite", "description": "my test suite", "scoring_method": "bertscore", "test_cases": [{"input": "this is test input to a language model", "reference_output": "this is test output from a language model"}, {"input": "this is another test prompt", "reference_output": "this is a test response"}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141"}'

@pytest.fixture(scope='session')
def mock_suite_request_optional_json():
    return '{"name": "test_suite", "description": null, "scoring_method": "bertscore", "test_cases": [{"input": "this is test input to a language model", "reference_output": "this is test output from a language model"}, {"input": "this is another test prompt", "reference_output": "this is a test response"}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141"}'''

@pytest.fixture(scope='session')
def mock_test_run():
    return TestRun(
        name="test_run",
        test_case_outputs=[
            TestCaseOutput(output='this is a test run output', score=0.8),
            TestCaseOutput(output='this is a good test run output', score=0.8),
            TestCaseOutput(output='this is a another test run output', score=0.8)
        ],
        model_name='my_very_special_gpt',
        created_at="2023-06-22T21:56:03.346141",
        created_by="arthur",
        bench_version="0.0.1",
    )

@pytest.fixture(scope='session')
def mock_test_run_json():
    return '''{"name": "test_run", "test_case_outputs": [{"id": null, "output": "this is a test run output", "score": 0.8}, {"id": null, "output": "this is a good test run output", "score": 0.8}, {"id": null, "output": "this is a another test run output", "score": 0.8}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141", "description": null, "model_name": "my_very_special_gpt", "foundation_model": null, "prompt_template": null, "model_version": null}'''