from .scoring_method import ScoringMethod
from .bertscore import BERTScore
from .qa_quality import QAQualityCorrectness
from .summary_quality import SummaryQuality
from .exact_match import ExactMatch

from arthur_bench.models.models import ScoringMethod as ScoringEnum


def load_scoring_method(name: ScoringEnum) -> ScoringMethod:
    if name == ScoringEnum.BERTScore:
        return BERTScore()
    elif name == ScoringEnum.SummaryQuality:
        return SummaryQuality()
    elif name == ScoringEnum.QACorrectness:
        return QAQualityCorrectness()
    elif name == ScoringEnum.ExactMatch:
        return ExactMatch()
    else:
        raise ValueError(f"scoring method {name} is not valid")
