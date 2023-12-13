from bert_score import BERTScorer
from typing import List, Optional
from arthur_bench.scoring import Scorer
from arthur_bench.scoring.utils import suppress_warnings
from arthur_bench.models.models import ScoreResult

DEFAULT_MODEL = "microsoft/deberta-v3-base"

DEFAULT_HEDGE = (
    "As an AI language model, I don't have personal opinions, emotions, or beliefs."
)


class HedgingLanguage(Scorer):
    """
    Given an input question and model output, determine if the output contains hedging
    language such as "As an AI language model, I don't have personal opinions, emotions,
    or beliefs". The values returned are a similarity score (BERTScore), with higher
    values corresponding to higher likelihood of hedging language being present in the
    model output.
    """

    def __init__(
        self, model_type: str = DEFAULT_MODEL, hedging_language: str = DEFAULT_HEDGE
    ):
        """
        Hedging Language score implementation.

        :param model_type: the underlying language model to extract embeddings from
        :param hedging_language: reference hedging language used by an llm
        """
        self.hedging_language = hedging_language

        with suppress_warnings("transformers"):
            self.scorer = BERTScorer(lang="en", model_type=model_type)

    @staticmethod
    def name() -> str:
        return "hedging_language"

    @staticmethod
    def requires_reference() -> bool:
        return False

    def to_dict(self, warn=False):
        return {
            "model_type": self.scorer.model_type,
            "hedging_language": self.hedging_language,
        }

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[ScoreResult]:
        # convert reference hedge to list
        reference_batch = [self.hedging_language] * len(candidate_batch)

        # get precision, recall, and F1 score from bert_score package
        p, r, f = self.scorer.score(candidate_batch, reference_batch, verbose=False)

        # return a BERTScore using F1
        list_bertscore = f.tolist()

        return [ScoreResult(score=score) for score in list_bertscore]
