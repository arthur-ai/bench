from typing import List, Optional
from arthur_bench.scoring import ScoringMethod
from arthur_bench.client.rest.client import ArthurClient
from arthur_bench.client.exceptions import ArthurUserError
from arthur_bench.models.scoring import HallucinationScoreRequest


class Hallucination(ScoringMethod):

    def __init__(self):
        self.client = ArthurClient()

    @staticmethod
    def name() -> str:
        return "hallucination"

    def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        if context_batch is None:
            raise ArthurUserError("context is required for hallucination scoring")

        res = []
        for i in range(len(candidate_batch)):
            req = HallucinationScoreRequest(response=candidate_batch[i], context=context_batch[i])

            # TODO: maybe add some retry logic here if you want
            score = self.client.bench.score_hallucination(req)
            res.append(float(score["hallucination"]))
        return res
