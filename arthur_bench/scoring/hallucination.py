from typing import List, Optional, Union
from arthur_bench.scoring import CategoricalScorer
from arthur_bench.client.rest.client import ArthurClient
from arthur_bench.exceptions import ArthurUserError
from arthur_bench.models.scoring import HallucinationScoreRequest


class Hallucination(CategoricalScorer):
    """
    Score each output against a context using Arthur's hosted hallucination checker
    A score of False means the scorer estimates the candidate is supported by the context
    A score of True means the scorer found information in the candidate unsupported by the context
    """

    def __init__(self):
        self.client = ArthurClient()

    @staticmethod
    def name() -> str:
        return "hallucination"
    
    @staticmethod
    def possible_values() -> List[bool]:
        return [True, False]

    @staticmethod
    def requires_reference() -> bool:
        return False

    def to_dict(self, warn=False):
        return {}

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[float]:
        if context_batch is None:
            raise ArthurUserError("context is required for hallucination scoring")

        res = []
        for i in range(len(candidate_batch)):
            request = HallucinationScoreRequest(
                response=candidate_batch[i], context=context_batch[i]
            )
            response = self.client.bench.score_hallucination(request)
            res.append(response.hallucination)
        return res
