import logging
from typing import Dict, List, Optional

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel

from arthur_bench.exceptions import UserValueError
from arthur_bench.scoring import CategoricalScorer
from arthur_bench.scoring.prompts.qa_correctness import DECIDE

logger = logging.getLogger(__name__)


class QAQualityCorrectness(CategoricalScorer):
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
    def categories() -> Dict[float, str]:
        return {0.0: "0", 1.0: "1", -1.0: "NA"}

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[float]:
        """
        Reference batch is not used for this scoring method, QA correctness requires an
        input_text_batch and context_batch
        """
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

        res = []
        for i in range(len(input_text_batch)):
            llmchoice = self.evaluator(
                {
                    "question": input_text_batch[i],
                    "context": context_batch[i],
                    "answer": candidate_batch[i],
                }
            )["text"]
            try:
                llmchoice = float(llmchoice)
            except ValueError:
                llmchoice = -1.0
            if llmchoice not in self.to_dict()["categories"]:
                llmchoice = -1.0
            res.append(llmchoice)
        return res
