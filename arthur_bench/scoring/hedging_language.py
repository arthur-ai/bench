from bert_score import BERTScorer
from typing import List, Optional
from arthur_bench.scoring import ScoringMethod
from arthur_bench.scoring.utils import suppress_warnings

DEFAULT_MODEL = "microsoft/deberta-v3-base"

# weight precision and recall differently
# for now, we have observed in experiments that
# recall is much more correlated with human judgment than precision
PRECISION_WEIGHT = 0.1
RECALL_WEIGHT = 0.9

# [TODO] need to make these editable by user
DEFAULT_HEDGE = "As an AI language model, I don't have personal opinions, emotions, or beliefs."
DEFAULT_THRESHOLD = 0.6

class HedgingLanguage(ScoringMethod):

    @staticmethod
    def name() -> str:
        return "hedging_language"
    
    @staticmethod
    def requires_reference() -> bool:
        return False

    def __init__(self, **kwargs):
        with suppress_warnings("transformers"):
            self.scorer = BERTScorer(lang='en', model_type=DEFAULT_MODEL)

    def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None,
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:

        # convert reference hedge to list
        reference_batch = [DEFAULT_HEDGE] * len(candidate_batch)

        # get precision, recall, and F1 score from bert_score package
        p, r, f = self.scorer.score(candidate_batch, reference_batch, verbose=False)

        # return a BERTScore using our weighting of precision and recall (instead of F1 which weights them equally)
        list_bertscore = (PRECISION_WEIGHT * p + RECALL_WEIGHT * r).tolist()

        # generate list of hedges based on threshold
        list_hedges = [float(n >= DEFAULT_THRESHOLD) for n in list_bertscore]

        return list_hedges
