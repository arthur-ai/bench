import uuid
from typing import Optional, List, Union
from arthur_bench.models.models import CreateRunRequest, TestCaseOutput, ScoreResult
from arthur_bench.client.bench_client import BenchClient
from arthur_bench.exceptions import ArthurUserError


class TestRun(CreateRunRequest):
    test_suite_id: uuid.UUID
    client: BenchClient  # type: ignore
    id: Optional[uuid.UUID] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def scores(self) -> List[Optional[float]]:
        return [case.score_result.score for case in self.test_cases]

    @property
    def categories(self) -> List[Optional[str]]:
        # we validate that all or None contain categories
        if self.test_cases[0].score_result.category is None:
            return [None for _ in range(len(self.test_cases))]
        return [case.score_result.category.name for case in self.test_cases]  # type: ignore # noqa

    @property
    def output(self) -> List[str]:
        return [case.output for case in self.test_cases]

    def save(self) -> uuid.UUID:
        """Save a test run."""
        if self.id is not None:
            raise ArthurUserError("run is already saved")

        resp = self.client.create_new_test_run(
            test_suite_id=str(self.test_suite_id),
            json_body=CreateRunRequest(**self.dict()),
        )
        self.id = resp.id
        return self.id

    @classmethod
    def from_flattened(
        cls,
        run_name: str,
        ids: List[uuid.UUID],
        candidate_output_list: List[str],
        scores: Union[List[float], List[ScoreResult]],
        client: BenchClient,
        test_suite_id: uuid.UUID,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        foundation_model: Optional[str] = None,
        prompt_template: Optional[str] = None,
    ):
        test_case_outputs = []
        for i, result in enumerate(scores):
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

        return cls(
            name=run_name,
            test_case_outputs=test_case_outputs,
            model_name=model_name,
            model_version=model_version,
            foundation_model=foundation_model,
            prompt_template=prompt_template,
            test_suite_id=test_suite_id,
            client=client,
        )
