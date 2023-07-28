from textstat import lexicon_count
from typing import List, Optional
from arthur_bench.scoring import ScoringMethod
from arthur_bench.scoring.utils import suppress_warnings



class WordCount(ScoringMethod):
    """
    Calculates number of words in each candidate output, removing the punctuation before counting.

    https://pypi.org/project/textstat/
    
    """

    def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None,
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:

        return [lexicon_count(i, removepunct=True) for i in candidate_batch]