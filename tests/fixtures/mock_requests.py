from arthur_bench.models.models import (
    TestSuiteRequest,
    TestCaseRequest,
    CreateRunRequest,
    TestCaseOutput,
)

MOCK_SUITE_CASES = [
    TestCaseRequest(
        input="this is test input to a language model",
        reference_output="this is test output from a language model",
    ),
    TestCaseRequest(
        input="this is another test prompt",
        reference_output="this is a test response",
    ),
]

MOCK_SUITE = TestSuiteRequest(
    name="test_suite",
    scoring_method={
        "name": "bertscore",
        "type": "built_in",
        "config": {
            "precision_weight": 0.1,
            "recall_weight": 0.9,
            "model_type": "microsoft/deberta-v3-base",
        },
    },
    created_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES,
)

MOCK_SUITE_CUSTOM = TestSuiteRequest(
    name="test_suite_custom",
    description="test_description",
    scoring_method={
        "name": "test_custom_scorer",
        "type": "custom",
        "config": {"custom_name": "param_name"},
    },
    created_at="2023-06-21T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
    test_cases=MOCK_SUITE_CASES,
)

MOCK_RUN = CreateRunRequest(
    name="test_run",
    test_cases=[
        TestCaseOutput(
            id="62d2d1b3-d7df-4999-b01c-52e93d34f576",
            output="this is a test run output",
            score=0.9,
        ),
        TestCaseOutput(
            id="70eb3014-2b04-4974-bb05-a2e20f2cf367",
            output="this is a good test run output",
            score=0.7,
        ),
    ],
    model_name="my_very_special_gpt",
    created_at="2023-06-22T21:56:03.346141",
    created_by="arthur",
    bench_version="0.0.1",
)

MOCK_SUITE_JSON = """{\
"name": "test_suite", \
"description": null, \
"scoring_method": {"name": "bertscore", "type": "built_in"}, \
"test_cases": [\
{\
"input": "this is test input to a language model", \
"reference_output": "this is test output from a language model"\
}, \
{\
"input": "this is another test prompt", \
"reference_output": "this is a test response"\
}\
]\
}"""

MOCK_RUN_JSON = """{"name": "test_run", "test_cases": [{"id": "62d2d1b3-d7df-4999-b01c-52e93d34f576", "output": "this is a test run output", "score": 0.9}, {"id": "70eb3014-2b04-4974-bb05-a2e20f2cf367", "output": "this is a good test run output", "score": 0.7}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141", "description": null, "model_name": "my_very_special_gpt", "foundation_model": null, "prompt_template": null, "model_version": null}"""

MOCK_RUN_JSON_REST = """{"name": "test_run", "test_case_outputs": [{"id": "62d2d1b3-d7df-4999-b01c-52e93d34f576", "output": "this is a test run output", "score": 0.9}, {"id": "70eb3014-2b04-4974-bb05-a2e20f2cf367", "output": "this is a good test run output", "score": 0.7}], "created_by": "arthur", "bench_version": "0.0.1", "created_at": "2023-06-22T21:56:03.346141", "description": null, "model_name": "my_very_special_gpt", "foundation_model": null, "prompt_template": null, "model_version": null}"""
