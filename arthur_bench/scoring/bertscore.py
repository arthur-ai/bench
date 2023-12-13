from bert_score import BERTScorer
from typing import List, Optional
from arthur_bench.scoring import Scorer
from arthur_bench.scoring.utils import suppress_warnings
from arthur_bench.models.models import ScoreResult

DEFAULT_MODEL = "microsoft/deberta-v3-base"

# weight precision and recall differently
# for now, we have observed in experiments that
# recall is much more correlated with human judgment than precision
PRECISION_WEIGHT = 0.1
RECALL_WEIGHT = 0.9


class BERTScore(Scorer):
    """
    Tailored bert score implementation.

    https://arxiv.org/abs/1904.09675
    """

    @staticmethod
    def name() -> str:
        return "bertscore"

    def __init__(self, model_type=DEFAULT_MODEL, precision_weight=PRECISION_WEIGHT):
        """
        Tailored bert score implementation.

        :param model_type: the underlying language model to extract embeddings from
        :param precision_weight: the weight given to the precision term in calculating
            bertscore
        """
        self.precision_weight = precision_weight
        self.recall_weight = 1 - precision_weight

        with suppress_warnings("transformers"):
            self.model = BERTScorer(lang="en", model_type=model_type)

    def to_dict(self, warn=False):
        return {
            "precision_weight": self.precision_weight,
            "model_type": self.model.model_type,
        }

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[ScoreResult]:
        # get precision, recall, and F1 score from bert_score package
        p, r, _ = self.model.score(candidate_batch, reference_batch, verbose=False)

        # return a BERTScore using our weighting of precision and recall (instead of F1
        # which weights them equally)
        return [
            ScoreResult(score=score)
            for score in (self.precision_weight * p + self.recall_weight * r).tolist()
        ]
