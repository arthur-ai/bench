from abc import abstractmethod, ABC
from typing import List, Optional

from tqdm import tqdm

from arthur_bench.models.models import TestCaseRequest

SINGLE_ITEM_BATCH_DEFAULT = 1


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

    def run(self, reference_outputs: List[str], candidate_outputs: List[str], inputs: Optional[List[str]] = None,
            contexts: Optional[List[str]] = None, batch_size: int = SINGLE_ITEM_BATCH_DEFAULT) -> List[float]:
        """
        Score a set of test cases. This method doesn't need to be implemented in most cases, but can be overriden to
        add additional functionality such as task-specific logging.

        :param reference_outputs: reference strings representing target outputs
        :param candidate_outputs: candidate generations to score
        :param inputs: input strings being tested
        :param contexts: optional corresponding contexts, if needed by scoring method
        :param batch_size: size of batches
        :return:
        """
        all_scores = []
        with tqdm(total=len(reference_outputs)) as pbar:
            for i in range(0, len(reference_outputs), batch_size):
                # TODO: make suite iterable: https://arthurai.atlassian.net/browse/LLM-250
                input_batch = list(inputs[i:i + batch_size]) if inputs is not None else None
                ref_batch = reference_outputs[i:i + batch_size]

                context_batch = None if contexts is None else contexts[i:i + batch_size]
                scores = self.run_batch(
                    list(ref_batch),
                    candidate_outputs[i:i + batch_size],
                    input_batch,
                    context_batch
                )

                all_scores.extend(scores)
                pbar.update(len(ref_batch))
    
        return all_scores
