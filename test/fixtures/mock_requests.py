from arthur_bench.models.models import TestSuiteRequest, TestCaseRequest, CreateRunRequest, TestCaseOutput

MOCK_SUITE_CASES = [
    TestCaseRequest(input="this is test input to a language model",
                    reference_output="this is test output from a language model"),
    TestCaseRequest(input="this is another test prompt",
                    reference_output="this is a test response")
]

MOCK_SUITE = TestSuiteRequest(
    name="test_suite",
    scoring_method={"name": "bertscore", "type": "built_in"},
    created_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES
)

MOCK_SUITE_CUSTOM = TestSuiteRequest(
    name="test_suite_custom",
    description="test_description",
    scoring_method={"name": "test_custom_scorer", "type": "custom"},
    created_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES
)

MOCK_RUN = CreateRunRequest(
    name="test_run",
    test_case_outputs=[
        TestCaseOutput(output='this is a test run output', score=0.8),
        TestCaseOutput(output='this is a good test run output', score=0.8),
    ],
    model_name='my_very_special_gpt',
    created_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
)