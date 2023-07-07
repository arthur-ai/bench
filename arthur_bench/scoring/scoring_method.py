from abc import abstractmethod, ABC
from typing import List, Optional


class ScoringMethod(ABC):
    """
    Base class for all scoring methods.     
    """
    @abstractmethod
    def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        """
        Score a batch of candidate generations.

        :param reference_batch: reference strings representing target outputs
        :param candidate_batch: candidate generations to score
        :param input_text_batch: optional corresponding inputs 
        :param context_batch: optional corresponding contexts, if needed by scoring method 
        """
        raise NotImplementedError
