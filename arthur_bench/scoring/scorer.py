from abc import abstractmethod, ABC
import sys
import asyncio
import json
import logging
from pathlib import Path
from typing import List, Optional, TypeVar, get_origin, get_args, Union
from inspect import signature, Parameter

from tqdm import tqdm
from arthur_bench.models.models import (
    ScoringMethodType,
    ScoreResult,
    Category,
    ScoringMethod,
    ScorerOutputType,
)


logger = logging.getLogger(__name__)


SINGLE_ITEM_BATCH_DEFAULT = 1
ASYNC_BATCH_DEFAULT = 5


TScorer = TypeVar("TScorer", bound="Scorer")


def _can_omit(parameter: Parameter):
    is_optional = get_origin(parameter.annotation) is Union and type(None) in get_args(
        parameter.annotation
    )
    is_kwargs = parameter.name == "args" or parameter.name == "kwargs"
    return is_optional or is_kwargs


class Scorer(ABC):
    """
    Base class for all scorers. Compute a float score for a given model generation.
    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        Get the name of this Scorer
        :return: the Scorer name
        """
        raise NotImplementedError

    @staticmethod
    def requires_reference() -> bool:
        """
        True if scorer requires reference output to compute score, False otherwise
        """
        return True

    @staticmethod
    def is_categorical() -> bool:
        """
        Whether the scorer is continuous or categorical.
        categories() should be implemented if True
        """
        return False

    @staticmethod
    def categories() -> Optional[List[Category]]:
        """
        All possible values returned by the scorer if output type is categorical.
        """
        return None

    @abstractmethod
    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> Union[List[float], List[ScoreResult]]:
        """
        Score a batch of candidate generations.

        :param candidate_batch: candidate generations to score
        :param reference_batch: reference strings representing target outputs
        :param input_text_batch: optional corresponding inputs
        :param context_batch: optional corresponding contexts, if needed by scorer
        :return: scoring results for this batch. Float scores are deprecated,
            use ScoreResult instead
        """
        raise NotImplementedError

    def run(
        self,
        candidate_outputs: List[str],
        reference_outputs: Optional[List[str]] = None,
        inputs: Optional[List[str]] = None,
        contexts: Optional[List[str]] = None,
        batch_size: int = SINGLE_ITEM_BATCH_DEFAULT,
    ) -> Union[List[float], List[ScoreResult]]:
        """
        Score a set of test cases. This method doesn't need to be implemented in most
        cases, but can be overriden to add additional functionality such as
        task-specific logging.

        :param candidate_outputs: candidate generations to score
        :param reference_outputs: reference strings representing target outputs
        :param inputs: input strings being tested
        :param contexts: optional corresponding contexts, if needed by scorer
        :param batch_size: size of batches
        :return: scoring results for this run. Float scores are deprecated,
            use ScoreResult instead
        """
        all_scores: Union[List[float], List[ScoreResult]] = []
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

                # validate run_batch results
                if self.is_categorical():
                    for score in scores:
                        if isinstance(score, float) or score.category is None:
                            raise ValueError(
                                "categorical scorer must return categorical results"
                            )

                all_scores.extend(scores)  # type: ignore
                pbar.update(len(candidate_outputs))

        return all_scores

    async def arun_batch(
        self,
        candidate_batch: List[str],
        reference_batch: Optional[List[str]] = None,
        input_text_batch: Optional[List[str]] = None,
        context_batch: Optional[List[str]] = None,
    ) -> Union[List[float], List[ScoreResult]]:
        """
        Async version of run_batch method.
        """
        raise NotImplementedError

    async def arun(
        self,
        candidate_outputs: List[str],
        reference_outputs: Optional[List[str]] = None,
        inputs: Optional[List[str]] = None,
        contexts: Optional[List[str]] = None,
        batch_size: int = ASYNC_BATCH_DEFAULT,
    ) -> Union[List[float], List[ScoreResult]]:
        """
        Async version of run method.
        """
        all_scores: Union[List[float], List[ScoreResult]] = []
        tasks = []
        for i in range(0, len(candidate_outputs), batch_size):
            input_batch = (
                list(inputs[i : i + batch_size]) if inputs is not None else None
            )
            ref_batch = (
                list(reference_outputs[i : i + batch_size])
                if reference_outputs is not None
                else None
            )

            context_batch = None if contexts is None else contexts[i : i + batch_size]
            task = asyncio.create_task(
                self.arun_batch(
                    candidate_outputs[i : i + batch_size],
                    ref_batch,
                    input_batch,
                    context_batch,
                )
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)  # returns tasks in order

        # validate arun_batch results and extend all_scores
        for scores in results:
            if self.is_categorical():
                for score in scores:
                    if isinstance(score, float) or score.category is None:
                        raise ValueError(
                            "categorical scorer must return categorical results"
                        )
            all_scores.extend(scores)  # type: ignore

        return all_scores

    def to_dict(self, warn=False):
        """
        Provides a json serializable representation of the scorer.
        """
        config = self.__dict__
        valid_args = [p for p in signature(self.__init__).parameters.values()]

        # warn if arguments missing from initialization for reloading
        for arg in valid_args:
            if not _can_omit(arg) and arg.name not in config:
                if warn:
                    logger.warning(
                        f"scorer requires argument {arg} but argument is not included "
                        "in json representation. this may effect test suite reloading, "
                        "consider implementing custom to_dict and from_dict methods"
                    )

        jsonable_config = {}
        # remove non serializable args
        for key, val in config.items():
            try:
                _ = json.dumps(val)
                jsonable_config[key] = val
            except TypeError:
                if warn:
                    logger.warning(
                        f"not including attribute {key} in config as it is not json"
                        "serializable. consider implementing custom to_dict and "
                        "from_dict methods"
                    )
        return jsonable_config

    @classmethod
    def from_dict(cls, config: dict):
        """
        Load a scorer from a json configuration file.
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
        Supplies whether a scorer is built-in or custom.

        This method is implemented by checking whether the Scorer class is part of the
        `arthur_bench.scoring` module.
        :return: the type (built-in or custom)
        """
        try:
            module = sys.modules[cls.__module__].__file__
            if module is not None:
                module_path = Path(module)
                if module_path.match("**/arthur_bench/scoring/**"):
                    return ScoringMethodType.BuiltIn
            return ScoringMethodType.Custom
        except AttributeError:
            return ScoringMethodType.Custom

    def to_metadata(self) -> ScoringMethod:
        return ScoringMethod(
            name=self.name(),
            type=self.type(),
            output_type=(
                ScorerOutputType.Categorical
                if self.is_categorical()
                else ScorerOutputType.Continuous
            ),
            categories=self.categories(),
            config=self.to_dict(warn=True),
        )
