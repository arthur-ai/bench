from enum import Enum
from typing import Dict

from .scorer import Scorer
from .bertscore import BERTScore
from .qa_quality import QAQualityCorrectness
from .summary_quality import SummaryQuality
from .exact_match import ExactMatch
from .hallucination import Hallucination
from .readability import Readability
from .word_count_match import WordCountMatch
from .specificity import Specificity
from .hedging_language import HedgingLanguage
from .python_unit_testing import PythonUnitTesting
from arthur_bench.exceptions import UserValueError


class ScoringMethodName(str, Enum):
    BERTScore = "bertscore"
    SummaryQuality = "summary_quality"
    QACorrectness = "qa_correctness"
    ExactMatch = "exact_match"
    Hallucination = "hallucination"
    Readability = "readability"
    WordCountMatch = "word_count_match"
    Specificity = "specificity"
    HedgingLanguage = "hedging_language"
    PythonUnitTesting = "python_unit_testing"


SCORING_METHOD_CLASS_MAP: Dict[str, type[Scorer]] = {
    ScoringMethodName.BERTScore: BERTScore,
    ScoringMethodName.QACorrectness: QAQualityCorrectness,
    ScoringMethodName.SummaryQuality: SummaryQuality,
    ScoringMethodName.ExactMatch: ExactMatch,
    ScoringMethodName.Hallucination: Hallucination,
    ScoringMethodName.Readability: Readability,
    ScoringMethodName.WordCountMatch: WordCountMatch,
    ScoringMethodName.Specificity: Specificity,
    ScoringMethodName.HedgingLanguage: HedgingLanguage,
    ScoringMethodName.PythonUnitTesting: PythonUnitTesting,
}


def scorer_from_string(method: str) -> type[Scorer]:
    if method in SCORING_METHOD_CLASS_MAP:
        return SCORING_METHOD_CLASS_MAP[method]
    else:
        raise UserValueError(f"Unknown scorer string {method}")
