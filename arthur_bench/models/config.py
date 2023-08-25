from enum import Enum
from typing import Callable, Optional, Union, Dict, Any
from dataclasses import dataclass

from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.llms import Cohere

from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain



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
class Prompt:
    name: Optional[str] = None
    system_message: Optional[str] = None
    instruction: Optional[str] = None

    def __str__(self):
        if self.name is not None:
            return self.name
        name = ''
        if self.system_message is not None:
            name += self.system_message
        if self.instruction is not None:
            name += self.instruction
        return name[:200]

    def to_template(self, model_type):
        if model_type == ModelType.COHERE_COMMAND or model_type == ModelType.COMMAND_LIGHT:
            if self.system_message is not None:
                raise ValueError("system message is not support with non chat models. Consider using model type gpt-3.5-turbo or claude-2")
            return PromptTemplate.from_template(
                f"""
                {self.instruction}
                Text: {{text}}
                """
            )
        
        messages = []
        if self.system_message is not None:
            messages.append(SystemMessagePromptTemplate.from_template(self.system_message))
        if self.instruction is not None:
            messages.append(HumanMessagePromptTemplate.from_template(self.instruction))
        messages.append(HumanMessagePromptTemplate.from_template('{text}'))
        return ChatPromptTemplate.from_messages(messages)

@dataclass
class LMConfig:
    model_name: Optional[ModelType] = None # see enum for valid model names
    model_function: Optional[Evaluator] = None # callable should return text or dict containing "text" field
    model_hyperparameters: Optional[Dict[str, Any]]= None
    prompt: Optional[Prompt] = None

    def __str___(self):
        model_version = ''
        if self.model_name is not None:
            model_version += self.model_name

        if self.model_function is not None:
            model_version += 'custom'

        if self.model_hyperparameters is not None:
            params = list(self.model_hyperparameters.items())[:3]
            for p in params:
                model_version += f'_{p[0]}={p[1]}'            


    def to_evaluator(self) -> Callable[[str], Union[str, Dict[str, str]]]:
        if self.model_name is None and self.model_function is None:
            raise ValueError("either model_name or model_function must be provided")
        
        if self.model_function is not None:
            return self.model_function

        config = {}
        if self.model_hyperparameters:
            config = self.model_hyperparameters
        
        prompt = self.prompt
        if prompt is None:
            prompt = Prompt()

        llm = MODEL_TYPE_TO_API[self.model_name](model_name = self.model_name, **config)
        return LLMChain(llm=llm, prompt=prompt.to_template(model_type=self.model_name))

ScoreConfig = Dict[float, str]

class EvaluatorConfig(LMConfig):
    score_config: ScoreConfig