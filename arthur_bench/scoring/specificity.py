from textstat import lexicon_count
from typing import List, Optional
from arthur_bench.scoring import Scorer
from wordfreq import word_frequency
from collections import Counter
import nltk
import re

from arthur_bench.models.models import ScoreResult


class Specificity(Scorer):
    """
    Returns a score from 0.0 to 1.0 indicating how specific the candidate output
    language is. Higher scores indicate that the language is more specific,
    Lower scores indicate more vague language.

    Specificity is computed through detecting words that indicate vagueness (predefined)
    determing how rare the words used are according to word frequencies calculated by
    popular nlp corpora, and detecting use of proper nouns and numbers.
    """

    @staticmethod
    def name() -> str:
        return "specificity"

    @staticmethod
    def requires_reference() -> bool:
        return False

    def __init__(self):
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")

    def get_num_vague_words(self, candidate_output: str) -> int:
        """
        Returns number of words in candidate_output which are is a list of pre-defined
        vague words.
        """
        vague_word_list = [
            "around",
            "about",
            "almost",
            "basically",
            "approximately",
            "nearly",
            "roughly",
            "some",
            "most",
            "least",
            "good",
            "bad",
            "nice",
            "great",
            "may",
            "could",
            "certain",
            "most",
            "might",
            "usually",
            "typically",
            "like",
            "sure",
        ]
        counter = 0
        candidate_output = candidate_output.lower()
        for v in vague_word_list:
            i = candidate_output.count(v)
            counter += i
        len_s = lexicon_count(candidate_output, removepunct=True)

        non_vague_prop = (
            len_s - counter
        ) / len_s  # proportion of words which are not vague
        non_vague_prop = (non_vague_prop / 0.2) - 4.0
        non_vague_prop = max(0.0, non_vague_prop)  # normalize
        return non_vague_prop

    def get_mean_word_freq(self, candidate_output: str) -> float:
        """
        Returns mean word frequency of candidate output. Higher values indicate that
        moree common words on average are used in the candidate output.
        Considers only words with frequency <0.001, truncating probability of words with
        higher frequencies to 0.001.
        """
        punct_regex = r"[^\w\s\'/]"
        # don't replace apostrophes
        text = re.sub(punct_regex, "", candidate_output)
        text = re.sub(r"[/]", " ", text)
        text_list = text.split()
        word_freqs = [word_frequency(word, "en") for word in text_list]

        # truncates all probability of words w freq >0.001 to 0.001
        filtered = [0.001 if i > 0.001 else i for i in word_freqs]
        if len(filtered) == 0:
            wf = 0.001
        else:
            wf = sum(filtered) / len(filtered)

        adj_freq = 2.0 - (wf / 0.0004)  # reverse scale and normalize
        adj_freq = max(0.0, adj_freq)
        adj_freq = min(1.0, adj_freq)

        return adj_freq

    def get_pn_and_num(self, candidate_output: str) -> int:
        """
        Returns total number of Proper Nouns and Numbers in candidate output.
        Determined heuristically via NNP and CD nltk tags.
        """
        # get number of proper nouns and numbers
        tokens = nltk.word_tokenize(candidate_output)
        tags = nltk.pos_tag(tokens)
        counts = Counter(tag for word, tag in tags)
        pn = counts["NNP"] + counts["CD"]
        len_s = lexicon_count(candidate_output, removepunct=True)
        pn_prop = 5.0 * (pn / len_s)
        pn_prop = min(1.0, pn_prop)
        return pn_prop

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[ScoreResult]:
        res = []
        for i in range(len(candidate_batch)):
            c = candidate_batch[i]

            vague_prop = self.get_num_vague_words(c)
            adj_freq = self.get_mean_word_freq(c)
            pn_prop = self.get_pn_and_num(c)

            s = (0.33 * vague_prop) + (0.33 * adj_freq) + (0.33 * pn_prop)  # aggregate
            res.append(ScoreResult(score=s))

        return res
