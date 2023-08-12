from typing import List, Optional

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from arthur_bench.scoring import ScoringMethod
from arthur_bench.scoring.prompts.qa_correctness import DECIDE
from arthur_bench.client.exceptions import UserValueError


class QAQualityCorrectness(ScoringMethod):
    """
    Given an input question, context string, and model generation, determine if the
    generation produced a correct answer.
    """

    def __init__(self):
        self.evaluate_answer = LLMChain(llm=ChatOpenAI(temperature=0), prompt=DECIDE)

    @staticmethod
    def name() -> str:
        return "qa_correctness"

    @staticmethod
    def requires_reference() -> bool:
        return False

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[float]:
        """
        Reference batch is not used for this scoring method, QA correctness requires
        an input_text_batch and context_batch
        """
        if input_text_batch is None:
            raise UserValueError(
                "input text is required for this scoring method. Please provide a"
                " dataframe column or a list of your input text strings in the Test"
                " Suite."
            )
        if context_batch is None:
            raise UserValueError(
                "context is required for this scoring method. Please provide a"
                " dataframe column or a list of your context strings in the Test Suite."
            )

        res = []
        for i in range(len(input_text_batch)):
            llmchoice = self.evaluate_answer(
                {
                    "question": input_text_batch[i],
                    "context": context_batch[i],
                    "answer": candidate_batch[i],
                }
            )["text"]
            if llmchoice not in ["0", "1", "NA"]:
                llmchoice = "-1"
            llmchoice = {"0": 0.0, "1": 1.0, "NA": -1.0, "-1": -1.0}[llmchoice]
            res.append(llmchoice)
        return res
