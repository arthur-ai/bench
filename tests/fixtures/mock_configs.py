from unittest import mock
from arthur_bench.models.config import LMConfig, Prompt
from langchain.llms.fake import FakeListLLM


class MockConfig(LMConfig):
    def to_evaluator(self):
        return FakeListLLM(
            responses=["this is a test run output", "this is a good test run output"]
        )


BASE_CONFIG = MockConfig(model_name="gpt-3.5-turbo")

CONFIG_WITH_PROMPT = MockConfig(
    model_name="gpt-3.5-turbo",
    prompt=Prompt(system_message="you are an expert", instruction="summarize this"),
)

CONFIG_WITH_CALLABLE = MockConfig(
    model_function=mock.Mock(return_value={"text": "model generated text"})
)

BASE_CONFIG_PARAMS = {
    "run_name": "auto_run",
    "candidate_output_list": [
        "this is a test run output",
        "this is a good test run output",
    ],
    "save": True,
    "batch_size": 1,
    "model_name": "gpt-3.5-turbo",
    "model_version": None,
    "foundation_model": "gpt-3.5-turbo",
    "prompt_template": None,
}

PROMPT_CONFIG_PARAMS = {
    "run_name": "auto_run",
    "candidate_output_list": [
        "this is a test run output",
        "this is a good test run output",
    ],
    "save": True,
    "batch_size": 1,
    "model_name": "gpt-3.5-turbo",
    "model_version": None,
    "prompt_template": "you are an expert summarize this",
    "foundation_model": "gpt-3.5-turbo",
}

CALLABLE_CONFIG_PARAMS = {
    "run_name": "auto_run",
    "candidate_output_list": [
        "this is a test run output",
        "this is a good test run output",
    ],
    "save": True,
    "batch_size": 1,
    "model_name": "custom",
    "model_version": None,
    "foundation_model": None,
    "prompt_template": None,
}
