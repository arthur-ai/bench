from textstat import lexicon_count
from typing import List, Optional

from arthur_bench.exceptions import UserTypeError
from arthur_bench.scoring import Scorer
from arthur_bench.models.models import ScoreResult


class WordCountMatch(Scorer):
    """
    Calculates how similar the number of words in the candidate output is to the the
    number of words in the reference output. Scores span from 0 to 1.
    A score of 1.0 indicates that there are the same number of words in the candidate
    output as in the reference output. Scores less than 1.0 are calculated as
    ((len_reference-delta)/len_reference) where delta is the absolute difference in
    word lengths between the candidate and reference outputs.
    All negative computed values are truncated to 0.
    Utilizes lexicon count, removing punctuations: https://pypi.org/project/textstat/

    """

    @staticmethod
    def name() -> str:
        return "word_count_match"

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[ScoreResult]:
        if reference_batch is None:
            raise UserTypeError(
                "Reference Outputs must be provided for Word Count Match scorer. "
                "Please provide reference outputs to the test suite"
            )
        word_count_match = []
        for i in range(len(reference_batch)):
            len_ref = lexicon_count(reference_batch[i], removepunct=True)
            len_cand = lexicon_count(candidate_batch[i], removepunct=True)
            delta = abs(len_ref - len_cand)
            if delta > len_ref:
                word_count_match.append(ScoreResult(score=0.0))
            else:
                word_count_match.append(ScoreResult(score=(len_ref - delta) / len_ref))

        return word_count_match
