import logging
import json
import pandas as pd
from typing import List, Optional, Union
from pathlib import Path

from tqdm import tqdm

from arthur_bench.scoring import ScoringMethod, scoring_method_class_from_string, ScoringMethodEnum
from arthur_bench.models.models import TestSuiteRequest, TestCaseOutput, ScoringMethod as ScoringMethodMetadata
from arthur_bench.client.exceptions import UserValueError, ArthurInternalError
from arthur_bench.run.testrun import TestRun
from arthur_bench.run.utils import _create_test_suite_dir, _initialize_metadata, _test_suite_dir, \
	_create_run_dir, _clean_up_run, _load_suite_from_args, _load_run_data_from_args, _get_suite_if_exists
from arthur_bench.scoring.scoring_method import SINGLE_ITEM_BATCH_DEFAULT, _create_run_dir, _clean_up_run, \
	_load_suite_from_args, _load_run_data_from_args, _get_suite_if_exists, _scoring_method_from_string


logger = logging.getLogger(__name__)


class TestSuite:
	"""
		Reusable pipeline for running a test suite built from reference_data and evaluated using metric

		:param name: name of the test suite
		:param scoring_method: scoring method to use to evaluate the results of a test run, as a string/enum or class
		:param description: short description of the task tested by this suite
		:param reference_data: dataframe of prompts and reference outputs
		:param reference_data_path: filepath to csv of prompts and reference outputs,
			required if not specifying reference_data
		:param input_column: the column of reference_data containing prompts, defaults to 'prompt'
		:param reference_column: the column of reference_data containing reference outputs, defaults to 'reference'
		:param input_text_list: list of strings of input texts that can be provided instead of dataframe columns
		:param reference_output_list: list of strings of reference outputs that can be provided instead of dataframe columns
	"""
	def __init__(
			self,
			name: str,
			scoring_method: Union[str, type[ScoringMethod]],
			description: Optional[str] = None,
			reference_data: Optional[pd.DataFrame] = None,
			reference_data_path: Optional[str] = None,
			input_column: str = "input",
			reference_column: str = "reference_output", 
			input_text_list: Optional[List[str]] = None,
			reference_output_list: Optional[List[str]] = None
	):
		self.id = None
		self.suite: Optional[TestSuiteRequest] = _get_suite_if_exists(name)

		if self.suite is None:
			# get a scoringMethod class
			if isinstance(scoring_method, str):
				scoring_method = _scoring_method_from_string(scoring_method=scoring_method)
			if scoring_method.name() == ScoringMethodEnum.QACorrectness:
				reference_column = None
			cases = _load_suite_from_args(
				reference_data=reference_data,
				reference_data_path=reference_data_path,
				input_column=input_column,
				reference_column=reference_column,
				input_text_list=input_text_list,
				reference_output_list=reference_output_list
			)
			self.suite = TestSuiteRequest(
				name=name,
				scoring_method=ScoringMethodMetadata(name=scoring_method.name(), type=scoring_method.type()),
				description=description,
				test_cases=cases,
				**_initialize_metadata()
			)
			self._test_suite_dir: Path = _create_test_suite_dir(name)

			# TODO: create scorer at self.scorer
		else:
			logger.info(f"Found existing test suite with name {name}. Using existing suite")
			self._test_suite_dir = _test_suite_dir(name)

			# TODO: load scorer at self.scorer

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
			prompt_template: Optional[str] = None

	) -> TestRun:
		"""
		Score a test run on candidate outputs.

		:param run_name: name for the test run
		:param candidate_data: dataframe of candidate responses to test prompts
		:param candidate_data_path: filepath to csv containing candidate responses to test prompts
		:param candidate_column: the column of candidate data containing candidate responses,
			defaults to 'candidate_output'
		:param candidate_output_list: list of strings of candidate outputs that can be provided instead of dataframe
		:param context_column: the column of reference_data containing supporting context for answering Question & Answering tasks
		:param context_list: list of strings containing supporting context for answering question and answering tasks
		:param save: whether to save the run results to file
		:param batch_size: the batch_size to use when computing scores
		:param model_name: model name for model used to generate outputs
		:param model_version: model version of model used to generate outputs
		:param foundation_model: foundation model name used to generate outputs
		:param prompt_template: prompt template name used to generate outputs
		:returns: TestRun object containing scored outputs
		"""
		candidate_output_list, context_list = _load_run_data_from_args(
			candidate_data=candidate_data,
			candidate_data_path=candidate_data_path,
			candidate_column=candidate_column,
			candidate_output_list=candidate_output_list,
			context_column=context_column,
			context_list=context_list,
		)

		if len(candidate_output_list) != len(self.suite.test_cases):
			raise UserValueError(
				f"candidate data has {len(candidate_output_list)} tests but expected {len(self.suite.test_cases)} tests")

		run_dir = None
		if save:
			run_dir = _create_run_dir(self.suite.name, run_name)

		scoring_method: ScoringMethod = _scoring_method_from_string(self.suite.scoring_method)

		inputs = [case.input for case in self.suite.test_cases]
		# ref outputs should be None if any items are None (we validate nullness must be all-or-none)
		ref_outputs: Optional[List[str]] = []
		if ref_outputs is not None:
			for case in self.suite.test_cases:
				if case.reference_output is None:
					ref_outputs = None
					break
				else:
					ref_outputs.append(case.reference_output)
		try:
			all_scores = self.scorer.run(candidate_output_list, ref_outputs, inputs, context_list,
										 batch_size=batch_size)
		except Exception as e:
			logger.error(f"failed to create run: {e}")
			if run_dir:
				_clean_up_run(run_dir=run_dir)
			raise ArthurInternalError(f"failed to create run {run_name}") from e
		
		test_case_outputs = [TestCaseOutput(output=output, score=score) for output, score in zip(candidate_output_list, all_scores)]
		
		run = TestRun(
			name=run_name,
			test_case_outputs=test_case_outputs,
			model_name=model_name,
			model_version=model_version,
			foundation_model=foundation_model,
			prompt_template=prompt_template,
			run_dir=run_dir,
			**_initialize_metadata()
		)

		if save:
			self.save()
			run.save()

		return run

	def save(self):
		"""Save a test suite to local file system."""
		suite_file = self._test_suite_dir / "suite.json"
		suite_file.write_text(self.suite.json())

		# TODO: serialize scorer
