from typing import List, Optional

from arthur_bench.exceptions import UserTypeError
from arthur_bench.scoring import Scorer
from arthur_bench.models.models import Category, ScoreResult


class ExactMatch(Scorer):
    """
    Returns 1 if candidate matches reference, 0 if candidate does not match reference.
    """

    def __init__(self, case_sensitive=True):
        self.case_sensitive = case_sensitive

    @staticmethod
    def name() -> str:
        return "exact_match"

    @staticmethod
    def is_categorical() -> bool:
        return True

    @staticmethod
    def categories() -> List[Category]:
        return [
            Category(
                name="non match",
                description="model output is different from reference output",
            ),
            Category(name="match", description="model output matches reference output"),
        ]

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[ScoreResult]:
        if reference_batch is None:
            raise UserTypeError(
                "Reference Outputs must be provided for Exact Match scorer. Please "
                "provide reference outputs to the test suite"
            )
        if self.case_sensitive:
            reference_batch = [ref.lower() for ref in reference_batch]
            candidate_batch = [cand.lower() for cand in candidate_batch]
        scores = [
            float(reference_batch[i] == candidate_batch[i])
            for i in range(len(reference_batch))
        ]
        return [
            ScoreResult(score=score, category=self.categories()[int(score)])
            for score in scores
        ]
