import logging
import tiktoken
from tiktoken.core import Encoding
from typing import Any, List, Optional, Tuple, Union, Dict
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel

from arthur_bench.exceptions import UserValueError, UserTypeError

from arthur_bench.scoring import Scorer
from arthur_bench.scoring.scorer import SINGLE_ITEM_BATCH_DEFAULT, ASYNC_BATCH_DEFAULT
from arthur_bench.scoring.prompts.summary_quality import COMPARE
from arthur_bench.models.models import Category, ScoreResult


CONTEXT_WINDOW_MAP = {
    "gpt-3.5-turbo": 4096,
    "gpt-4": 8192,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-4-32k": 32768,
}
EVALUATOR_MODEL = "gpt-3.5-turbo"
TIKTOKEN_ENCODER = tiktoken.get_encoding("cl100k_base")
TIKTOKEN_ERROR_PADDING = 150
LLM_CHOICE_TO_FLOAT = {"0": 0.0, "1": 1.0, "tie": 0.5}
LLM_CHOICE_TO_CATEGORIES = {
    "0": Category(
        name="reference",
        description="reference summary preferred",
    ),
    "1": Category(
        name="candidate",
        description="candidate summary preferered",
    ),
    "tie": Category(name="equal", description="summaries are equally preferred"),
    "default": Category(name="invalid", description="invalid response from llm grader"),
}

logger = logging.getLogger(__name__)


def truncate_input_text(
    input_text,
    ref_output,
    cand_output,
    context_window: int = CONTEXT_WINDOW_MAP[EVALUATOR_MODEL],
    tokenizer: Encoding = TIKTOKEN_ENCODER,
) -> Tuple[str, bool]:
    """Truncates the input_text to fit in LLM evaluator context

    Truncate the input text so that the filled-in COMPARE prompt
    which contains {input text + summary A + summary B} fits in the evaluator context
    window

    Returns the tuple (text, whether text was truncated)
    """
    llm_prompt_untruncated = COMPARE.format(
        text=input_text, summary_A=ref_output, summary_B=cand_output
    )
    input_text_tokens = tokenizer.encode(input_text)
    llm_prompt_tokens = tokenizer.encode(llm_prompt_untruncated)
    num_to_truncate_from_input_text_tokens = (
        len(llm_prompt_tokens) - context_window + TIKTOKEN_ERROR_PADDING
    )
    truncated = False
    if num_to_truncate_from_input_text_tokens > 0:
        input_text_tokens_truncated = input_text_tokens[
            :-num_to_truncate_from_input_text_tokens
        ]
        input_text = tokenizer.decode(input_text_tokens_truncated)
        truncated = True
    return input_text, truncated


class SummaryQuality(Scorer):
    """
    Comprehensive measure of summarization quality compared to a reference summary.
    """

    def __init__(
        self,
        llm: Optional[BaseChatModel] = None,
        context_window: int = CONTEXT_WINDOW_MAP[EVALUATOR_MODEL],
        tokenizer: Optional[Encoding] = None,
    ):
        if llm is None:
            llm = ChatOpenAI(temperature=0)
        if tokenizer is None:
            tokenizer = TIKTOKEN_ENCODER

        if not isinstance(llm, BaseChatModel):
            # Customization is fine, but warn that it should be a chat model
            logger.warning(
                "Custom LLM is allowed, but unexpected results may occur if it is not a"
                " chat model"
            )
        self.evaluator = LLMChain(llm=llm, prompt=COMPARE)
        self.context_window = context_window
        self.tokenizer = tokenizer

    @staticmethod
    def name() -> str:
        return "summary_quality"

    @staticmethod
    def is_categorical() -> bool:
        return True

    @staticmethod
    def categories() -> List[Category]:
        return list(LLM_CHOICE_TO_CATEGORIES.values())

    def to_dict(self, warn=False):
        return {}

    def _truncate_inputs(self, inputs, reference_outputs, candidate_outputs):
        # truncate inputs if needed
        truncated_inputs = []
        num_truncated = 0
        for i in range(len(inputs)):
            inp, truncated = truncate_input_text(
                inputs[i],
                reference_outputs[i],
                candidate_outputs[i],
                self.context_window,
                self.tokenizer,
            )
            num_truncated += int(truncated)

            # add to list we'll actually use
            truncated_inputs.append(inp)

        if num_truncated > 0:
            logger.warning(
                f"Truncated {num_truncated} out of {len(inputs)} total summary inputs "
                f"to {self.context_window} characters"
            )
        return truncated_inputs

    async def arun(
        self,
        candidate_outputs: List[str],
        reference_outputs: Optional[List[str]] = None,
        inputs: Optional[List[str]] = None,
        contexts: Optional[List[str]] = None,
        batch_size: int = ASYNC_BATCH_DEFAULT,
    ) -> Union[List[float], List[ScoreResult]]:
        if inputs is None:
            raise UserValueError(
                "input text is required for this scorer. Please provide a dataframe "
                "column or a list of your "
                "input text strings in the Test Suite."
            )
        if reference_outputs is None:
            raise UserTypeError(
                "Reference Outputs must be provided for Summary Quality scorer. Please "
                "provide reference outputs to the test suite"
            )

        if contexts is not None:
            raise UserValueError(
                "using context is not currently supported for summary quality"
            )
        truncated_inputs = self._truncate_inputs(
            inputs, reference_outputs, candidate_outputs
        )

        return await super().arun(
            candidate_outputs, reference_outputs, truncated_inputs, contexts, batch_size
        )

    def run(
        self,
        candidate_outputs: List[str],
        reference_outputs: Optional[List[str]] = None,
        inputs: Optional[List[str]] = None,
        contexts: Optional[List[str]] = None,
        batch_size: int = SINGLE_ITEM_BATCH_DEFAULT,
    ) -> Union[List[ScoreResult], List[float]]:
        truncated_inputs = self._truncate_inputs(
            inputs, reference_outputs, candidate_outputs
        )

        return super().run(
            candidate_outputs, reference_outputs, truncated_inputs, contexts, batch_size
        )

    def _parse_response(self, response: Dict[str, Any]) -> ScoreResult:
        llmchoice = response["text"][:3] if "text" in response else None

        if llmchoice in LLM_CHOICE_TO_FLOAT:
            return ScoreResult(
                score=LLM_CHOICE_TO_FLOAT[llmchoice],
                category=LLM_CHOICE_TO_CATEGORIES[llmchoice],
            )
        else:
            return ScoreResult(score=-1.0, category=LLM_CHOICE_TO_CATEGORIES["default"])

    @staticmethod
    def validate_batch(
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> Tuple[List[str], List[str]]:
        if input_text_batch is None:
            raise UserValueError(
                "input text is required for this scorer. Please provide a dataframe "
                "column or a list of your "
                "input text strings in the Test Suite."
            )
        if reference_batch is None:
            raise UserTypeError(
                "Reference Outputs must be provided for Summary Quality scorer. Please "
                "provide reference outputs to the test suite"
            )

        if context_batch is not None:
            raise UserValueError(
                "using context is not currently supported for summary quality"
            )
        return input_text_batch, reference_batch

    async def arun_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> Union[List[float], List[ScoreResult]]:
        """
        Summary quality requires input_text_batch. Asynchronous implementation
        """
        input_text_batch, reference_batch = self.validate_batch(
            candidate_batch, reference_batch, input_text_batch, context_batch
        )
        res = []
        for i in range(len(input_text_batch)):
            # run LLMChain to choose whether summary A or summary B is a better summary
            # of the input text

            choice = await self.evaluator.acall(
                {
                    "text": input_text_batch[i],
                    "summary_A": reference_batch[i],
                    "summary_B": candidate_batch[i],
                }
            )

            res.append(self._parse_response(choice))

        return res

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[ScoreResult]:
        """
        Summary quality requires input_text_batch.
        """
        input_text_batch, reference_batch = self.validate_batch(
            candidate_batch, reference_batch, input_text_batch, context_batch
        )
        res = []
        for i in range(len(input_text_batch)):
            # run LLMChain to choose whether summary A or summary B is a better summary
            # of the input text

            choice = self.evaluator(
                {
                    "text": input_text_batch[i],
                    "summary_A": reference_batch[i],
                    "summary_B": candidate_batch[i],
                }
            )

            res.append(self._parse_response(choice))
        return res
