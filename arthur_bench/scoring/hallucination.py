from typing import List, Optional
from arthur_bench.scoring import Scorer
from arthur_bench.client.rest.client import ArthurClient
from arthur_bench.exceptions import ArthurUserError
from arthur_bench.models.scoring import HallucinationScoreRequest

from arthur_bench.models.models import Category, ScoreResult


class Hallucination(Scorer):
    """
    Score each output against a context using Arthur's hosted hallucination checker
    A score of 1.0 means the hallucination checker estimates the output is supported by
    the context
    A score of 0.0 means the hallucination checker found information in the output
    unsupported by the context
    """

    def __init__(self):
        self.client = ArthurClient()

    @staticmethod
    def name() -> str:
        return "hallucination"

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
                name="hallucination",
                description="model output not supported by context",
            ),
            Category(
                name="no hallucination", description="model output supported by context"
            ),
        ]

    def to_dict(self, warn=False):
        return {}

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[ScoreResult]:
        if context_batch is None:
            raise ArthurUserError("context is required for hallucination scoring")

        res = []
        for i in range(len(candidate_batch)):
            request = HallucinationScoreRequest(
                response=candidate_batch[i], context=context_batch[i]
            )
            response = self.client.bench.score_hallucination(request)
            # score 0 if there is a hallucination, 1 if no hallucination found
            score = float(not response.hallucination)
            res.append(ScoreResult(score=score, category=self.categories()[int(score)]))
        return res
