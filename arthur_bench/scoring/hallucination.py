from typing import List, Optional
from arthur_bench.scoring import ScoringMethod
from arthur_bench.client.rest.client import ArthurClient
from arthur_bench.client.exceptions import ArthurUserError
from arthur_bench.models.scoring import HallucinationScoreRequest


class Hallucination(ScoringMethod):
    """
    Score each output against a context using Arthur's hosted hallucination checker
    A score of 1.0 means the hallucination checker estimates the output is supported by the context
    A score of 0.0 means the hallucination checker found information in the output unsupported by the context
    """

    def __init__(self):
        self.client = ArthurClient()

    @staticmethod
    def name() -> str:
        return "hallucination"
    
    @staticmethod
    def requires_reference() -> bool:
        return False

    def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None, 
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        if context_batch is None:
            raise ArthurUserError("context is required for hallucination scoring")

        res = []
        for i in range(len(candidate_batch)):
            request = HallucinationScoreRequest(response=candidate_batch[i], context=context_batch[i])
            response = self.client.bench.score_hallucination(request)
            score = float(response["hallucination"])
            res.append(score)
        return res
