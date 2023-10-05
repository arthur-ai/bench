from textstat import flesch_reading_ease
from typing import List, Optional
from arthur_bench.scoring import Scorer, Feedback

# specified by the flesch reading score github
# https://github.com/textstat/textstat
max_flesch_reading_ease_value = 121.22


class Readability(Scorer):
    """
    Flesch Reading Ease Score: the higher the score, the easier to read.
    Scores of 100-90 correlate to a 5th grade reading level, while scores <10 are
    classified as "Extremely difficult to read, and best understood by university
    graduates."

    https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
    """

    @staticmethod
    def name() -> str:
        return "readability"

    @staticmethod
    def requires_reference() -> bool:
        return False

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[Feedback]:
        """Use the flesch reading ease function,
        cut off negative values and divide by max value to get score between 0 and 1"""

        return [
            Feedback(score=max(flesch_reading_ease(i), 0) / max_flesch_reading_ease_value)
            for i in candidate_batch
        ]
