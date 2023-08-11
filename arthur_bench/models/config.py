from enum import Enum
from typing import Callable, Optional, Union, Dict, Any
from dataclasses import dataclass

from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.llms import Cohere


class ModelType(str, Enum):
    GPT_35_TURBO = 'gpt-3.5-turbo'
    GPT_4 = 'gpt-4'
    GPT_35_TURBO_16k = 'gpt-3.5-turbo-16k'
    GPT_4_32K = 'gpt-4-32k'
    COHERE_COMMAND = 'co-command'
    COMMAND_LIGHT = 'co-command-light'
    CLAUDE = 'claude'
    CLAUDE_2 = 'claude-2'

MODEL_TYPE_TO_API = {
    ModelType.GPT_35_TURBO : ChatOpenAI,
    ModelType.GPT_35_TURBO_16k: ChatOpenAI,
    ModelType.GPT_4: ChatOpenAI,
    ModelType.GPT_4_32K: ChatOpenAI,
    ModelType.COHERE_COMMAND: Cohere,
    ModelType.COMMAND_LIGHT: Cohere,
    ModelType.CLAUDE: ChatAnthropic,
    ModelType.CLAUDE_2: ChatAnthropic
}

Evaluator = Callable[[str], Union[str, Dict[str, str]]]

@dataclass
class LMConfig:
    model_name: ModelType # see enum for valid model names
    # model_function: Optional[Evaluator] = None # callable should return text or dict containing "text" field
    model_hyperparameters: Optional[Dict[str, Any]]= None
    # endpoint: str
    # prompt: Optional[str] = None

    def to_evaluator(self) -> Callable[[str], Union[str, Dict[str, str]]]:
        config = {}
        if self.model_hyperparameters:
            config = self.model_hyperparameters
        return MODEL_TYPE_TO_API[self.model_name](model_name = self.model_name, **config)
