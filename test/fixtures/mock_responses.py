from arthur_bench.models.models import (
    PaginatedTestSuite,
    TestCaseResponse,
    PaginatedTestSuites,
    TestSuiteMetadata,
    PaginatedRuns,
    TestRunMetadata,
    PaginatedRun,
    RunResult,
    SummaryItem,
    HistogramItem,
    TestSuiteSummary,
)

MOCK_BERTSCORE_CONFIG = {
    "precision_weight": 0.1,
    "recall_weight": 0.9,
    "model_type": "microsoft/deberta-v3-base",
}

MOCK_SUITE_CASES = [
    TestCaseResponse(
        id="62d2d1b3-d7df-4999-b01c-52e93d34f576",
        input="this is test input to a language model",
        reference_output="this is test output from a language model",
    ),
    TestCaseResponse(
        id="70eb3014-2b04-4974-bb05-a2e20f2cf367",
        input="this is another test prompt",
        reference_output="this is a test response",
    ),
]


MOCK_SUITE_CASES_WITH_NULL = [
    TestCaseResponse(
        id="62d2d1b3-d7df-4999-b01c-52e93d34f576",
        input="this is test input to a language model",
    ),
    TestCaseResponse(
        id="70eb3014-2b04-4974-bb05-a2e20f2cf367", input="this is another test prompt"
    ),
]



MOCK_SUITE_RESPONSE = PaginatedTestSuite(
    id="8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    name="test_suite",
    scoring_method={
        "name": "bertscore",
        "type": "built_in",
        "config": MOCK_BERTSCORE_CONFIG,
    },
    created_at="2023-06-22T21:56:03.346141",
    updated_at="2023-06-22T21:56:03.346141",
    test_cases=MOCK_SUITE_CASES,
)

MOCK_SUITE_RESPONSE_WITH_PAGES = PaginatedTestSuite(
    id="8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    name="test_suite",
    scoring_method={
        "name": "bertscore",
        "type": "built_in",
        "config": MOCK_BERTSCORE_CONFIG,
    },
    created_at="2023-06-22T21:56:03.346141",
    updated_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES,
    page=1,
    page_size=5,
    total_pages=1,
    total_count=2,
)

MOCK_SUITE_WITH_NULL = PaginatedTestSuite(
    id="8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    name="test_suite",
    scoring_method={
        "name": "bertscore",
        "type": "built_in",
        "config": MOCK_BERTSCORE_CONFIG,
    },
    created_at="2023-06-22T21:56:03.346141",
    updated_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES_WITH_NULL,
)

MOCK_SUITE_WITH_SCORING_CONFIG = PaginatedTestSuite(
    id="8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    name="test_suite",
    scoring_method={
        "name": "bertscore",
        "type": "built_in",
        "config": {"scoring_param": "my_custom_param"},
    },
    created_at="2023-06-22T21:56:03.346141",
    updated_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES_WITH_NULL,
)

MOCK_SUITE_JSON = '{"id": "8b7ba080-8d14-42d2-9250-ec0edb96abd7", "name": "test_suite", "scoring_method": {"name": "bertscore", "type": "built_in", "config": {"precision_weight": 0.1, "recall_weight": 0.9, "model_type": "microsoft/deberta-v3-base"}}, "test_cases": [{"id": "62d2d1b3-d7df-4999-b01c-52e93d34f576", "input": "this is test input to a language model", "reference_output": "this is test output from a language model"}, {"id": "70eb3014-2b04-4974-bb05-a2e20f2cf367", "input": "this is another test prompt", "reference_output": "this is a test response"}], "created_at": "2023-06-22T21:56:03.346141", "updated_at": "2023-06-22T21:56:03.346141", "description": null, "last_run_time": null, "num_runs": 0, "page": null, "page_size": null, "total_pages": null, "total_count": null}'

MOCK_SUITE_WITH_NULL_JSON = '{"id": "8b7ba080-8d14-42d2-9250-ec0edb96abd7", "name": "test_suite", "scoring_method": {"name": "bertscore", "type": "built_in", "config": {"precision_weight": 0.1, "recall_weight": 0.9, "model_type": "microsoft/deberta-v3-base"}}, "test_cases": [{"id": "62d2d1b3-d7df-4999-b01c-52e93d34f576", "input": "this is test input to a language model", "reference_output": null}, {"id": "70eb3014-2b04-4974-bb05-a2e20f2cf367", "input": "this is another test prompt", "reference_output": null}], "created_at": "2023-06-22T21:56:03.346141", "updated_at": "2023-06-22T21:56:03.346141", "description": null, "last_run_time": null, "num_runs": 0, "page": null, "page_size": null, "total_pages": null, "total_count": null}'

MOCK_SUITE_WITH_SCORING_JSON = '{"id": "8b7ba080-8d14-42d2-9250-ec0edb96abd7", "name": "test_suite", "scoring_method": {"name": "bertscore", "type": "built_in", "config": {"scoring_param": "my_custom_param"}}, "test_cases": [{"id": "62d2d1b3-d7df-4999-b01c-52e93d34f576", "input": "this is test input to a language model", "reference_output": null}, {"id": "70eb3014-2b04-4974-bb05-a2e20f2cf367", "input": "this is another test prompt", "reference_output": null}], "created_at": "2023-06-22T21:56:03.346141", "updated_at": "2023-06-22T21:56:03.346141", "description": null, "last_run_time": null, "num_runs": 0, "page": null, "page_size": null, "total_pages": null, "total_count": null}'

MOCK_SUITE_CUSTOM_RESPONSE = PaginatedTestSuite(
    id="87772642-df15-46d0-b6e5-c68407b21ee3",
    name="test_suite_custom",
    description="test_description",
    scoring_method={
        "name": "test_custom_scorer",
        "type": "custom",
        "config": {"custom_name": "param_name"},
    },
    created_at="2023-06-21T21:56:03.346141",
    updated_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES,
)

MOCK_NO_SUITES = PaginatedTestSuites(
    test_suites=[], page=1, page_size=5, total_count=0, total_pages=1
)

MOCK_SUITES = PaginatedTestSuites(
    test_suites=[
        TestSuiteMetadata(
            id="8b7ba080-8d14-42d2-9250-ec0edb96abd7",
            name="test_suite",
            scoring_method={
                "name": "bertscore",
                "type": "built_in",
                "config": MOCK_BERTSCORE_CONFIG,
            },
            created_at="2023-06-22T21:56:03.346141",
            updated_at="2023-06-22T21:56:03.346141",
        )
    ],
    page=1,
    page_size=5,
    total_count=1,
    total_pages=1,
)

MOCK_SUITES_ALL = PaginatedTestSuites(
    test_suites=[
        TestSuiteMetadata(
            id="87772642-df15-46d0-b6e5-c68407b21ee3",
            name="test_suite_custom",
            scoring_method={
                "name": "test_custom_scorer",
                "type": "custom",
                "config": {"custom_name": "param_name"},
            },
        ),
        TestSuiteMetadata(
            id="8b7ba080-8d14-42d2-9250-ec0edb96abd7",
            name="test_suite",
            scoring_method={
                "name": "bertscore",
                "type": "built_in",
                "config": MOCK_BERTSCORE_CONFIG,
            },
        ),
    ],
    page=1,
    page_size=5,
    total_count=2,
    total_pages=1,
)

MOCK_SUITES_CUSTOM_ONLY = PaginatedTestSuites(
    test_suites=[
        TestSuiteMetadata(
            id="87772642-df15-46d0-b6e5-c68407b21ee3",
            name="test_suite_custom",
            scoring_method={
                "name": "test_custom_scorer",
                "type": "custom",
                "config": {"custom_name": "param_name"},
            },
        ),
    ],
    page=1,
    page_size=5,
    total_count=1,
    total_pages=1,
)

MOCK_RUNS_RESPONSE = PaginatedRuns(
    test_runs=[
        TestRunMetadata(
            id="af8466a8-6425-4ea5-85cb-ed952b26fa6c",
            name="test_run",
            created_at="2023-06-22T21:56:03.346141",
            updated_at="2023-06-22T21:56:03.346141",
            avg_score=0.8,
        )
    ],
    test_suite_id="8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    page=1,
    page_size=5,
    total_count=1,
    total_pages=1,
)

MOCK_RUN_RESULTS = [
    RunResult(
        id="70eb3014-2b04-4974-bb05-a2e20f2cf367",
        input="this is another test prompt",
        reference_output="this is a test response",
        output="this is a good test run output",
        score=0.7,
    ),
    RunResult(
        id="62d2d1b3-d7df-4999-b01c-52e93d34f576",
        input="this is test input to a language model",
        reference_output="this is test output from a language model",
        output="this is a test run output",
        score=0.9,
    ),
]

MOCK_RUN_RESPONSE = PaginatedRun(
    id="af8466a8-6425-4ea5-85cb-ed952b26fa6c",
    test_suite_id="8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    name="test_run",
    created_at="2023-06-22T21:56:03.346141",
    updated_at="2023-06-22T21:56:03.346141",
    test_cases=MOCK_RUN_RESULTS,
    page=1,
    page_size=5,
    total_count=2,
    total_pages=1,
)

MOCK_SUMMARY = SummaryItem(
    id="af8466a8-6425-4ea5-85cb-ed952b26fa6c",
    name="my_test_run",
    avg_score=0.8,
    histogram=[HistogramItem(count=2, low=0, high=0.8)],
)

MOCK_SUMMARY_RESPONSE = TestSuiteSummary(
    summary=[MOCK_SUMMARY],
    num_test_cases=2,
    page=1,
    page_size=5,
    total_pages=1,
    total_count=1,
)

MOCK_SUITES_JSON = {
    "page": 1,
    "page_size": 5,
    "test_suites": [
        {
            "created_at": "2023-06-22T21:56:03.346141",
            "description": None,
            "id": "8b7ba080-8d14-42d2-9250-ec0edb96abd7",
            "last_run_time": None,
            "name": "test_suite",
            "scoring_method": {
                "name": "bertscore",
                "type": "built_in",
                "config": MOCK_BERTSCORE_CONFIG,
            },
            "updated_at": "2023-06-22T21:56:03.346141",
        }
    ],
    "total_pages": 1,
    "total_count": 1,
}

MOCK_SUITE_RESPONSE_JSON = {
    "created_at": "2023-06-22T21:56:03.346141",
    "description": None,
    "id": "8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    "last_run_time": None,
    "name": "test_suite",
    "num_runs": 0,
    "last_run_time": None,
    "scoring_method": "bertscore",
    "test_cases": [
        {
            "id": "62d2d1b3-d7df-4999-b01c-52e93d34f576",
            "input": "this is test input to a language model",
            "reference_output": "this is test output from a language model",
        },
        {
            "id": "70eb3014-2b04-4974-bb05-a2e20f2cf367",
            "input": "this is another test prompt",
            "reference_output": "this is a test response",
        },
    ],
    "page": 1,
    "page_size": 5,
    "total_pages": 1,
    "total_count": 2,
    "updated_at": "2023-06-22T21:56:03.346141",
}

MOCK_RUNS_RESPONSE_JSON = {
    "page": 1,
    "page_size": 5,
    "test_runs": [
        {
            "avg_score": 0.8,
            "created_at": "2023-06-22T21:56:03.346141",
            "id": "af8466a8-6425-4ea5-85cb-ed952b26fa6c",
            "model_version": None,
            "name": "test_run",
            "prompt_template": None,
            "updated_at": "2023-06-22T21:56:03.346141",
        }
    ],
    "test_suite_id": "8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    "total_count": 1,
    "total_pages": 1,
}

MOCK_SUMMARY_RESPONSE_JSON = {
    "num_test_cases": 2,
    "page": 1,
    "page_size": 5,
    "summary": [
        {
            "avg_score": 0.8,
            "histogram": [{"count": 2, "high": 0.8, "low": 0.0}],
            "id": "af8466a8-6425-4ea5-85cb-ed952b26fa6c",
            "name": "my_test_run",
        }
    ],
    "total_count": 1,
    "total_pages": 1,
}

MOCK_RUN_RESPONSE_JSON = {
    "created_at": "2023-06-22T21:56:03.346141",
    "id": "af8466a8-6425-4ea5-85cb-ed952b26fa6c",
    "name": "test_run",
    "page": 1,
    "page_size": 5,
    "test_case_runs": [
        {
            "id": "70eb3014-2b04-4974-bb05-a2e20f2cf367",
            "input": "this is another test prompt",
            "output": "this is a good test run output",
            "reference_output": "this is a test response",
            "score": 0.7,
        },
        {
            "id": "62d2d1b3-d7df-4999-b01c-52e93d34f576",
            "input": "this is test input to a language model",
            "output": "this is a test run output",
            "reference_output": "this is test output from a language model",
            "score": 0.9,
        },
    ],
    "test_suite_id": "8b7ba080-8d14-42d2-9250-ec0edb96abd7",
    "total_count": 2,
    "total_pages": 1,
    "updated_at": "2023-06-22T21:56:03.346141",
}
