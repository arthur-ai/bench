import pytest
import pandas as pd
from arthur_bench.models.models import TestSuiteRequest, TestCaseRequest, TestCaseOutput, PaginatedTestSuite, PaginatedTestSuites
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
def mock_suite_cases_no_ref():
    return [
            TestCaseRequest(input="this is test input to a language model",
                            reference_output=None),
            TestCaseRequest(input="this is another test prompt",
                            reference_output=None)
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
def mock_suite_request_optional(mock_suite_cases_no_ref):
    return TestSuiteRequest(
        name="test_suite",
        scoring_method="bertscore",
        created_at="2023-06-22T21:56:03.346141",
        created_by="arthur",
        bench_version="0.0.1",
        test_cases=mock_suite_cases_no_ref
    )

@pytest.fixture(scope='session')
def mock_suite_request_json():
    return '{"name": "test_suite", "description": "my test suite", "scoring_method": {"name": "bertscore", "type": "built_in"}, "test_cases": [{"input": "this is test input to a language model", "reference_output": "this is test output from a language model"}, {"input": "this is another test prompt", "reference_output": "this is a test response"}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141"}'

@pytest.fixture(scope='session')
def mock_suite_request_optional_json():
    return '{"name": "test_suite", "description": null, "scoring_method": {"name": "bertscore", "type": "built_in"}, "test_cases": [{"input": "this is test input to a language model", "reference_output": null}, {"input": "this is another test prompt", "reference_output": null}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141"}'''

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


@pytest.fixture
def mock_summary_data():
    return pd.DataFrame(
        {
            'source': [
                'Breaking News: Earthquake measuring 7.2 magnitude strikes California. The earthquake originated near the city of Los Angeles and was felt across the region. Several buildings have collapsed, and there are reports of injuries and casualties. Rescue operations are underway.',
                'Just had the most amazing dinner at this new restaurant in town! The food was delicious, and the service was top-notch. I highly recommend it to everyone looking for a great dining experience.',
                'New study reveals the benefits of regular exercise. According to the research, engaging in physical activity for at least 30 minutes a day can significantly reduce the risk of heart disease, obesity, and other chronic conditions. Start incorporating exercise into your daily routine!',
                'Exciting announcement: The company is launching a new product next month. Stay tuned for more details and be among the first to experience this innovative offering.',
            ],
            'summary': [
                'A powerful earthquake hits California, causing damage and casualties.',
                'An enthusiastic review of a new restaurant in town with excellent food and service.',
                'Recent study highlights the positive impact of regular exercise on health.',
                'The company plans to release a new product, generating anticipation among customers.'
            ],
            'candidate_summary': [
                'Massive earthquake strikes California, causing destruction and loss of life.',
                'Had dinner at a new restaurant. Food and service were great!',
                'Exercise has health benefits and can reduce the risk of diseases.',
                'Exciting news: New product launch coming soon!'
            ]
        }
    )