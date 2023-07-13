from enum import Enum
from typing import Dict

from .scoring_method import ScoringMethod
from .bertscore import BERTScore
from .qa_quality import QAQualityCorrectness
from .summary_quality import SummaryQuality
from .exact_match import ExactMatch
from ..client.exceptions import UserValueError


# TODO: naming
class ScoringMethodEnum(str, Enum):
    BERTScore = 'bertscore'
    SummaryQuality = 'summary_quality'
    QACorrectness = 'qa_correctness'


SCORING_METHOD_CLASS_MAP: Dict[str, type[ScoringMethod]] = {
    ScoringMethodEnum.BERTScore: BERTScore,
    ScoringMethodEnum.QACorrectness: QAQualityCorrectness,
    ScoringMethodEnum.SummaryQuality: SummaryQuality
}


def scoring_method_class_from_string(method: str) -> type[ScoringMethod]:
    if method in SCORING_METHOD_CLASS_MAP:
        return SCORING_METHOD_CLASS_MAP[method]
    else:
        raise UserValueError(f"Unknown ScoringMethod string {method}")
