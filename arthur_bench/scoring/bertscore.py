from bert_score import BERTScorer
from typing import List, Optional
from arthur_bench.scoring import ScoringMethod
from arthur_bench.scoring.utils import suppress_warnings
from arthur_bench.client.exceptions import UserTypeError

DEFAULT_MODEL = "microsoft/deberta-v3-base"

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

    @staticmethod
    def name() -> str:
        return "bertscore"

    def __init__(self, model_type=DEFAULT_MODEL, precision_weight=PRECISION_WEIGHT, recall_weight=RECALL_WEIGHT):
        self.precision_weight = precision_weight
        self.recall_weight = recall_weight

        with suppress_warnings("transformers"):
            self.scorer = BERTScorer(lang='en', model_type=model_type)

    def to_dict(self):
        return {"precision_weight": self.precision_weight, "recall_weight": self.recall_weight, "model_type": self.scorer.model_type}

    def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None,
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:

        # get precision, recall, and F1 score from bert_score package
        p, r, f = self.scorer.score(candidate_batch, reference_batch, verbose=False)

        # return a BERTScore using our weighting of precision and recall (instead of F1 which weights them equally)
        return (self.precision_weight * p + self.recall_weight * r).tolist()
