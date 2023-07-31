from enum import Enum
from typing import Dict

from .scoring_method import ScoringMethod
from .bertscore import BERTScore
from .qa_quality import QAQualityCorrectness
from .summary_quality import SummaryQuality
from .exact_match import ExactMatch
from .hallucination import Hallucination
from ..client.exceptions import UserValueError


class ScoringMethodEnum(str, Enum):
    BERTScore = 'bertscore'
    SummaryQuality = 'summary_quality'
    QACorrectness = 'qa_correctness'
    ExactMatch = 'exact_match'
    Hallucination = 'hallucination'


SCORING_METHOD_CLASS_MAP: Dict[str, type[ScoringMethod]] = {
    ScoringMethodEnum.BERTScore: BERTScore,
    ScoringMethodEnum.QACorrectness: QAQualityCorrectness,
    ScoringMethodEnum.SummaryQuality: SummaryQuality,
    ScoringMethodEnum.ExactMatch: ExactMatch,
    ScoringMethodEnum.Hallucination: Hallucination
}


def scoring_method_class_from_string(method: str) -> type[ScoringMethod]:
    if method in SCORING_METHOD_CLASS_MAP:
        return SCORING_METHOD_CLASS_MAP[method]
    else:
        raise UserValueError(f"Unknown ScoringMethod string {method}")
