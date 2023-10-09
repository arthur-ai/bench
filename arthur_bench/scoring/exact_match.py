from typing import List, Optional

from arthur_bench.exceptions import UserTypeError
from arthur_bench.scoring import CategoricalScorer, Feedback


class ExactMatch(CategoricalScorer):
    """
    Returns True if candidate matches reference,
    False if candidate does not match reference.
    """

    def __init__(self, case_sensitive=True):
        self.case_sensitive = case_sensitive

    @staticmethod
    def name() -> str:
        return "exact_match"

    @staticmethod
    def categories() -> List[str]:
        return ["True", "False"]

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[Feedback]:
        if reference_batch is None:
            raise UserTypeError(
                "Reference Outputs must be provided for Exact Match scorer. Please "
                "provide reference outputs to the test suite"
            )
        if not self.case_sensitive:
            return [
                Feedback(
                    label=str(reference_batch[i].lower() == candidate_batch[i].lower())
                )
                for i in range(len(reference_batch))
            ]
        return [
            Feedback(label=str(reference_batch[i] == candidate_batch[i]))
            for i in range(len(reference_batch))
        ]
