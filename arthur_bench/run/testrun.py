import uuid
from typing import Optional, List
from arthur_bench.models.models import CreateRunRequest
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
        return [case.score_result.category.name for case in self.test_cases]  # type: ignore

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
