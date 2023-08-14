from typing import List, Optional

from arthur_bench.client.exceptions import UserTypeError
from arthur_bench.scoring import ScoringMethod


class ExactMatch(ScoringMethod):
    """
    Returns 1 if candidate matches reference, 0 if candidate does not match reference.
    """
    def __init__(self, case_sensitive=True):
        self.case_sensitive = case_sensitive

    @staticmethod
    def name() -> str:
        return "exact_match"

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[float]:
        if reference_batch is None:
            raise UserTypeError(
                "Reference Outputs must be provided for Exact Match scorer. Please provide "
                "reference outputs to the test suite"
            )
        if not self.case_sensitive:
            return [
                float(reference_batch[i].lower() == candidate_batch[i].lower())
                for i in range(len(reference_batch))
            ]
        return [
            float(reference_batch[i] == candidate_batch[i])
            for i in range(len(reference_batch))
        ]
