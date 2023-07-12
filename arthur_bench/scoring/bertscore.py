from bert_score import BERTScorer
from typing import List, Optional
from arthur_bench.scoring import ScoringMethod
from arthur_bench.scoring.utils import suppress_warnings

DEFAULT_MODEL = "t5-base"

# weight precision and recall differently
# for now, we have observed in experiments that
# recall is much more correlated with human judgment than precision
PRECISION_WEIGHT = 0.1
RECALL_WEIGHT = 0.9


class BERTScore(ScoringMethod):
    """
    Tailored bert score implementation.
    
    https://arxiv.org/abs/1904.09675
    """

    def __init__(self):
        self.scorer = BERTScorer(lang='en', model_type=DEFAULT_MODEL)

    def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:

        # get precision, recall, and F1 score from bert_score package
        with suppress_warnings("transformers"):
            p, r, f = self.scorer.score(candidate_batch, reference_batch, verbose=False)

        # return a BERTScore using our weighting of precision and recall (instead of F1 which weights them equally)
        return (PRECISION_WEIGHT * p + RECALL_WEIGHT * r).tolist()
