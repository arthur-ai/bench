from .scoring_method import ScoringMethod
from .bertscore import BERTScore
from .qa_quality import QAQualityCorrectness
from .summary_quality import SummaryQuality
from .exact_match import ExactMatch
from .reading_ease import ReadingEase
from .word_count import WordCount

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
    elif name == ScoringEnum.ReadingEase:
        return ReadingEase()
    elif name == ScoringEnum.WordCount:
        return WordCount()
    else:
        raise ValueError(f"scoring method {name} is not valid")
