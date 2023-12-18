import logging
import pandas as pd
from typing import List, Optional, Union
from arthur_bench.scoring import Scorer
from arthur_bench.models.models import (
    TestSuiteRequest,
    PaginatedTestSuite,
    TestCaseOutput,
    ScoringMethodType,
    TestCaseResponse,
    ScoreResult,
)
from arthur_bench.exceptions import (
    UserValueError,
    ArthurInternalError,
)
from arthur_bench.client import BenchClient, _get_bench_client
from arthur_bench.run.testrun import TestRun
from arthur_bench.run.utils import (
    _load_suite_from_args,
    _load_run_data_from_args,
    _initialize_scorer,
)

from arthur_bench.scoring.scorer import SINGLE_ITEM_BATCH_DEFAULT


logger = logging.getLogger(__name__)


class TestSuite:
    """
    Reusable pipeline for running a test suite built from reference_data and evaluated
    using scoring_method

    :param name: name of the test suite
    :param scoring_method: scoring method or scorer instance to use to evaluate the
        results of a test run, as a string/enum or class instance
    :param description: short description of the task tested by this suite
    :param reference_data: dataframe of prompts and reference outputs
    :param reference_data_path: filepath to csv of prompts and reference outputs,
            required if not specifying reference_data
    :param input_column: the column of reference_data containing prompts, defaults to
        'prompt'
    :param reference_column: the column of reference_data containing reference outputs,
        defaults to 'reference'
    :param input_text_list: list of strings of input texts that can be provided instead
        of dataframe columns
    :param reference_output_list: list of strings of reference outputs that can be
        provided instead of dataframe columns
    """

    def __init__(
        self,
        name: str,
        scoring_method: Union[str, Scorer],
        description: Optional[str] = None,
        reference_data: Optional[pd.DataFrame] = None,
        reference_data_path: Optional[str] = None,
        input_column: str = "input",
        reference_column: str = "reference_output",
        input_text_list: Optional[List[str]] = None,
        reference_output_list: Optional[List[str]] = None,
        client: Optional[BenchClient] = None,
    ):
        self._data: PaginatedTestSuite
        if client is None:
            client = _get_bench_client()
        self.client = client
        suite = client.get_suite_if_exists(name=name)
        self.scorer: Scorer

        if suite is None:
            self.scorer = _initialize_scorer(scoring_method_arg=scoring_method)
            cases = _load_suite_from_args(
                reference_data=reference_data,
                reference_data_path=reference_data_path,
                input_column=input_column,
                reference_column=reference_column,
                input_text_list=input_text_list,
                reference_output_list=reference_output_list,
                requires_reference=self.scorer.requires_reference(),
            )
            method_meta = self.scorer.to_metadata()
            new_suite = TestSuiteRequest(
                name=name,
                scoring_method=method_meta,
                description=description,
                test_cases=cases,
            )
            self._data = self.client.create_test_suite(new_suite)

        else:
            logger.info(
                f"Found existing test suite with name {name}. Using existing suite"
            )

            self._data = suite
            if self._data.scoring_method.type == ScoringMethodType.Custom:
                if isinstance(scoring_method, str):
                    raise UserValueError(
                        "cannot reference custom scorer by string. please provide "
                        "instantiated scorer"
                    )

                self.scorer = scoring_method
                if self.scorer.name() != self._data.scoring_method.name:
                    raise UserValueError(
                        f"Test suite was originally created with scorer: "
                        f"{self._data.scoring_method.name}"
                        f"but provided scorer: {scoring_method.name()}"
                    )
                if self.scorer.to_dict() != self._data.scoring_method.config:
                    logger.warning(
                        "scorer configuration has changed from test suite creation."
                    )
            else:
                self.scorer = _initialize_scorer(
                    self._data.scoring_method.name, self._data.scoring_method.config
                )

    @property
    def name(self) -> str:
        return self._data.name

    @property
    def description(self) -> Optional[str]:
        return self._data.description

    @property
    def test_cases(self) -> List[TestCaseResponse]:
        return self._data.test_cases

    @property
    def input_texts(self) -> List[str]:
        return [case.input for case in self._data.test_cases]

    @property
    def reference_outputs(self) -> List[Optional[str]]:
        return [case.reference_output for case in self._data.test_cases]

    @property
    def scoring_method(self) -> str:
        return self.scorer.name()

    def run(
        self,
        run_name: str,
        candidate_data: Optional[pd.DataFrame] = None,
        candidate_data_path: Optional[str] = None,
        candidate_column: str = "candidate_output",
        candidate_output_list: Optional[List[str]] = None,
        context_column: Optional[str] = None,
        context_list: Optional[List[str]] = None,
        save: bool = True,
        batch_size: int = SINGLE_ITEM_BATCH_DEFAULT,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        foundation_model: Optional[str] = None,
        prompt_template: Optional[str] = None,
    ) -> TestRun:
        """
        Score a test run on candidate outputs.

        :param run_name: name for the test run
        :param candidate_data: dataframe of candidate responses to test prompts
        :param candidate_data_path: filepath to csv containing candidate responses to
            test prompts
        :param candidate_column: the column of candidate data containing candidate
            responses, defaults to 'candidate_output'
        :param candidate_output_list: list of strings of candidate outputs that can be
            provided instead of dataframe
        :param context_column: the column of reference_data containing supporting
            context for answering Question & Answering tasks
        :param context_list: list of strings containing supporting context for answering
             question and answering tasks
        :param save: whether to save the run results to file
        :param batch_size: the batch_size to use when computing scores
        :param model_name: model name for model used to generate outputs
        :param model_version: model version of model used to generate outputs
        :param foundation_model: foundation model name used to generate outputs
        :param prompt_template: prompt template name used to generate outputs
        :returns: TestRun object containing scored outputs
        """

        # make sure no existing test run named run_name is already attached to this
        #  suite
        if self.client.check_run_exists(str(self._data.id), run_name):
            raise UserValueError(
                f"A test run with the name {run_name} already exists. "
                "Give this test run a unique name and re-run."
            )

        candidate_output_list, context_list = _load_run_data_from_args(
            candidate_data=candidate_data,
            candidate_data_path=candidate_data_path,
            candidate_column=candidate_column,
            candidate_output_list=candidate_output_list,
            context_column=context_column,
            context_list=context_list,
        )

        if len(candidate_output_list) != len(self.test_cases):
            raise UserValueError(
                f"candidate data has {len(candidate_output_list)} tests but "
                f"expected {len(self.test_cases)} tests"
            )

        inputs = self.input_texts
        ids = [case.id for case in self.test_cases]
        # ref outputs should be None if any items are None (we validate nullness must be
        #  all-or-none)
        ref_outputs: Optional[List[str]] = []
        if ref_outputs is not None:
            for case in self.test_cases:
                if case.reference_output is None:
                    ref_outputs = None
                    break
                else:
                    ref_outputs.append(case.reference_output)
        try:
            all_scores = self.scorer.run(
                candidate_output_list,
                ref_outputs,
                inputs,
                context_list,
                batch_size=batch_size,
            )
        except Exception as e:
            logger.error(f"failed to create run: {e}")
            raise ArthurInternalError(f"failed to create run {run_name}") from e

        test_case_outputs = []
        for i, result in enumerate(all_scores):
            # temporary hack until score field is fully deprecated
            score: Optional[float] = (
                result if isinstance(result, float) else result.score  # type: ignore
            )
            # we can't properly type this in python3.9. In 3.10 we can switch to
            # https://github.com/python/mypy/issues/11934#issuecomment-1008295539
            score_result: ScoreResult = (
                ScoreResult(score=result) if isinstance(result, float) else result  # type: ignore # noqa
            )  # type: ignore
            test_case_outputs.append(
                TestCaseOutput(
                    id=ids[i],
                    output=candidate_output_list[i],
                    score=score,
                    score_result=score_result,
                )
            )

        run = TestRun(
            name=run_name,
            test_case_outputs=test_case_outputs,
            model_name=model_name,
            model_version=model_version,
            foundation_model=foundation_model,
            prompt_template=prompt_template,
            test_suite_id=self._data.id,
            client=self.client,
        )

        if save:
            run.save()

        return run

    def save(self):
        """Save a test suite to local file system."""
        suite_file = self._test_suite_dir / "suite.json"
        suite_file.write_text(self._data.json())
