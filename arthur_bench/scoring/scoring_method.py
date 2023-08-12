from abc import abstractmethod, ABC
import sys
from typing import List, Optional, TypeVar

from tqdm import tqdm

from arthur_bench.models.models import ScoringMethodType

SINGLE_ITEM_BATCH_DEFAULT = 1


TScoringMethod = TypeVar("TScoringMethod", bound="ScoringMethod")


class ScoringMethod(ABC):
    """
    Base class for all scoring methods.
    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        Get the name of this ScoringMethod
        :return: the ScoringMethod name
        """
        raise NotImplementedError

    @staticmethod
    def requires_reference() -> bool:
        return True

    @abstractmethod
    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> List[float]:
        """
        Score a batch of candidate generations.

        :param candidate_batch: candidate generations to score
        :param reference_batch: reference strings representing target outputs
        :param input_text_batch: optional corresponding inputs
        :param context_batch: optional corresponding contexts, if needed by scoring method
        """
        raise NotImplementedError

    def run(
        self,
        candidate_outputs: List[str],
        reference_outputs: Optional[List[str]] = None,
        inputs: Optional[List[str]] = None,
        contexts: Optional[List[str]] = None,
        batch_size: int = SINGLE_ITEM_BATCH_DEFAULT,
    ) -> List[float]:
        """
        Score a set of test cases. This method doesn't need to be implemented in most cases, but can be overriden to
        add additional functionality such as task-specific logging.

        :param candidate_outputs: candidate generations to score
        :param reference_outputs: reference strings representing target outputs
        :param inputs: input strings being tested
        :param contexts: optional corresponding contexts, if needed by scoring method
        :param batch_size: size of batches
        :return:
        """
        all_scores = []
        with tqdm(total=len(candidate_outputs)) as pbar:
            for i in range(0, len(candidate_outputs), batch_size):
                # TODO: make suite iterable: https://arthurai.atlassian.net/browse/LLM-250
                input_batch = (
                    list(inputs[i : i + batch_size]) if inputs is not None else None
                )
                ref_batch = (
                    list(reference_outputs[i : i + batch_size])
                    if reference_outputs is not None
                    else None
                )

                context_batch = (
                    None if contexts is None else contexts[i : i + batch_size]
                )
                scores = self.run_batch(
                    candidate_outputs[i : i + batch_size],
                    ref_batch,
                    input_batch,
                    context_batch,
                )

                all_scores.extend(scores)
                pbar.update(len(candidate_outputs))

        return all_scores

    @classmethod
    def type(cls) -> ScoringMethodType:
        """
        Supplies whether a scoring method is built-in or custom.

        This method is implemented by checking whether the ScoringMethod class is part of the `arthur_bench.scoring`
        module.
        :return: the type (built-in or custom)
        """
        try:
            module = sys.modules[cls.__module__].__file__
            if module is not None and "arthur_bench/scoring" in module:
                return ScoringMethodType.BuiltIn
            else:
                return ScoringMethodType.Custom
        except AttributeError:
            return ScoringMethodType.Custom
