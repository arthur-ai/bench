from bert_score import BERTScorer
from typing import List, Optional
from arthur_bench.scoring import ScoringMethod
from arthur_bench.scoring.utils import suppress_warnings

DEFAULT_MODEL = "microsoft/deberta-v3-base"

# [TODO] need to make these editable by user
DEFAULT_HEDGE = "As an AI language model, I don't have personal opinions, emotions, or beliefs."

class HedgingLanguage(ScoringMethod):
    """
    Given an input question and model output, determine if the output contains hedging language 
    such as "As an AI language model, I don't have personal opinions, emotions, or beliefs". 
    The values returned are a similarity score (BERTScore), with higher values corresponding to
    higher likelihood of hedging language being present in the model output.
    """

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

        # return a BERTScore using F1
        list_bertscore = f.tolist()

        return list_bertscore
