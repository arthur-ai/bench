from arthur_bench.models.models import TestSuiteResponse, TestCaseResponse, \
    PaginatedGetTestSuitesResponse, TestSuite, PaginatedGetTestSuiteResponse

MOCK_SUITE_CASES = [
    TestCaseResponse(input="this is test input to a language model",
                    reference_output="this is test output from a language model"),
    TestCaseResponse(input="this is another test prompt",
                    reference_output="this is a test response")
]

MOCK_SUITE = TestSuiteResponse(
    id='8b7ba080-8d14-42d2-9250-ec0edb96abd7',
    name="test_suite",
    description="my test suite",
    scoring_method={"name": "bertscore", "type": "built_in"},
    created_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES
)

MOCK_NO_SUITES = PaginatedGetTestSuitesResponse(test_suites=[])

MOCK_SUITES = PaginatedGetTestSuitesResponse(test_suites=[
    TestSuite(
        id='8b7ba080-8d14-42d2-9250-ec0edb96abd7',
        name="test_suite",
        scoring_method={"name": "bertscore", "type": "built_in"},
    )
])

MOCK_EXISTING_SUITE = PaginatedGetTestSuiteResponse(
    id='8b7ba080-8d14-42d2-9250-ec0edb96abd7',
    name="test_suite",
    scoring_method={"name": "bertscore", "type": "built_in"},
    test_cases=MOCK_SUITE_CASES
)