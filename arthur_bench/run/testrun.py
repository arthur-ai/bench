import uuid
from typing import Optional
from arthur_bench.models.models import CreateRunRequest
from arthur_bench.client.bench_client import BenchClient
from arthur_bench.client.exceptions import ArthurUserError


class TestRun(CreateRunRequest):
    test_suite_id: uuid.UUID
    client: BenchClient  # type: ignore
    id: Optional[uuid.UUID]

    class Config:
        arbitrary_types_allowed = True

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
