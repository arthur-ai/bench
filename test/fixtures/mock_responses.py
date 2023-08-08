from arthur_bench.models.models import PaginatedTestSuite, TestCaseResponse, \
    PaginatedTestSuites, TestSuiteMetadata

MOCK_SUITE_CASES = [
    TestCaseResponse(
        id='62d2d1b3-d7df-4999-b01c-52e93d34f576',
        input="this is test input to a language model",
        reference_output="this is test output from a language model"),
    TestCaseResponse(
        id='70eb3014-2b04-4974-bb05-a2e20f2cf367',
        input="this is another test prompt",
        reference_output="this is a test response")
]

MOCK_SUITE = PaginatedTestSuite(
    id='8b7ba080-8d14-42d2-9250-ec0edb96abd7',
    name="test_suite",
    description="my test suite",
    scoring_method={"name": "bertscore", "type": "built_in"},
    created_at="2023-06-22T21:56:03.346141",
    updated_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES
)

MOCK_NO_SUITES = PaginatedTestSuites(test_suites=[], page=1, page_size=1, total_count=0, total_pages=1)

MOCK_SUITES = PaginatedTestSuites(test_suites=[
    TestSuiteMetadata(
        id='8b7ba080-8d14-42d2-9250-ec0edb96abd7',
        name="test_suite",
        scoring_method={"name": "bertscore", "type": "built_in"},
    )
], page=1, page_size=1, total_count=1, total_pages=1)