import logging
from typing import List, Optional, Dict, Any, Union, Tuple

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel

from arthur_bench.exceptions import UserValueError
from arthur_bench.scoring import Scorer
from arthur_bench.scoring.prompts.qa_correctness import DECIDE
from arthur_bench.models.models import Category, ScoreResult


logger = logging.getLogger(__name__)


class QAQualityCorrectness(Scorer):
    """
    Given an input question, context string, and model generation, determine if the
    generation produced a correct answer.
    """

    def __init__(self, llm: Optional[BaseChatModel] = None):
        if llm is None:
            llm = ChatOpenAI(temperature=0)
        else:
            # Customization is fine, but warn that it should be a chat model
            logger.warning(
                "Custom LLM is allowed, but unexpected results may occur if it is not a"
                " chat model"
            )
        self.evaluator = LLMChain(llm=llm, prompt=DECIDE)

    @staticmethod
    def name() -> str:
        return "qa_correctness"

    @staticmethod
    def requires_reference() -> bool:
        return False

    @staticmethod
    def is_categorical() -> bool:
        return True

    @staticmethod
    def categories() -> List[Category]:
        return [
            Category(
                name="incorrect",
                description="model output is incorrect given the context",
            ),
            Category(
                name="correct", description="model output is correct given the context"
            ),
            Category(name="invalid", description="grader returned an invalid response"),
        ]

    def to_dict(self, warn=False):
        return {}

    def _parse_response(self, response: Dict[str, Any]) -> ScoreResult:
        llmchoice = response["text"]
        if llmchoice not in ["0", "1", "NA"]:
            llmchoice = "-1"
        llmchoice = {"0": 0.0, "1": 1.0, "NA": -1.0, "-1": -1.0}[llmchoice]
        return ScoreResult(score=llmchoice, category=self.categories()[int(llmchoice)])

    @staticmethod
    def validate_batch(
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> Tuple[List[str], List[str]]:
        if input_text_batch is None:
            raise UserValueError(
                "input text is required for this scoring method. Please provide a "
                "dataframe column or a list of your input text strings in the Test "
                "Suite."
            )
        if context_batch is None:
            raise UserValueError(
                "context is required for this scoring method. Please provide a "
                "dataframe column or a list of your context strings in the Test Suite."
            )

        if reference_batch is not None:
            raise UserValueError(
                "using reference is not currently supported for qa correctness"
            )
        return input_text_batch, context_batch

    async def arun_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> Union[List[float], List[ScoreResult]]:
        """
        Reference batch is not used for this scoring method, QA correctness requires an
        input_text_batch and context_batch
        """
        input_text_batch, context_batch = self.validate_batch(
            candidate_batch, reference_batch, input_text_batch, context_batch
        )
        res = []
        for i in range(len(input_text_batch)):
            llmchoice = await self.evaluator.acall(
                {
                    "question": input_text_batch[i],
                    "context": context_batch[i],
                    "answer": candidate_batch[i],
                }
            )
            res.append(self._parse_response(llmchoice))
        return res

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[ScoreResult]:
        """
        Reference batch is not used for this scoring method, QA correctness requires an
        input_text_batch and context_batch
        """
        input_text_batch, context_batch = self.validate_batch(
            candidate_batch, reference_batch, input_text_batch, context_batch
        )

        res = []
        for i in range(len(input_text_batch)):
            llmchoice = self.evaluator(
                {
                    "question": input_text_batch[i],
                    "context": context_batch[i],
                    "answer": candidate_batch[i],
                }
            )
            res.append(self._parse_response(llmchoice))
        return res
