from typing import List, Optional
from arthur_bench.scoring import ScoringMethod


class ExactMatch(ScoringMethod):

    def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:

        return [float(reference_batch[i] == candidate_batch[i]) for i in range(len(reference_batch))]