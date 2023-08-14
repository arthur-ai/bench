from abc import abstractmethod, ABC
import sys
import json
import logging
from typing import List, Optional, TypeVar, get_origin, get_args, Union
from inspect import signature

from tqdm import tqdm
from arthur_bench.models.models import ScoringMethodType


logger = logging.getLogger(__name__)


SINGLE_ITEM_BATCH_DEFAULT = 1


TScoringMethod = TypeVar("TScoringMethod", bound="ScoringMethod")


def _is_optional(field):
    return get_origin(field) is Union and type(None) in get_args(field)


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
        :return: array of scores for batch
        """
        all_scores = []
        with tqdm(total=len(candidate_outputs)) as pbar:
            for i in range(0, len(candidate_outputs), batch_size):
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

    def to_dict(self):
        """
        Provides a json serializable representation of the scoring method.
        """
        config = self.__dict__
        valid_args = [p for p in signature(self.__init__).parameters.values()]

        # warn if arguments missing from initialization for reloading
        for arg in valid_args:
            if not _is_optional(arg.annotation) and arg.name not in config:
                logger.warning(
                    f"scoring method requires argument {arg} but argument is not included in json representation. "
                    "this may effect test suite reloading, consider implementing custom to_dict and from_dict methods"
                )

        jsonable_config = {}
        # remove non serializable args
        for key, val in config.items():
            try:
                _ = json.dumps(val)
                jsonable_config[key] = val
            except TypeError as e:
                logger.warning(
                    f"not including attribute {key} in config as it is not json serializable. "
                    "consider implementing custom to_dict and from_dict methods"
                )
        return jsonable_config

    @classmethod
    def from_dict(cls, config: dict):
        """
        Load a scoring method from a json configuration file.
        """
        valid_args = [p for p in signature(cls.__init__).parameters.keys()]

        init_config = {}
        for key, value in config.items():
            if key in valid_args:
                init_config[key] = value
        return cls(**init_config)

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
