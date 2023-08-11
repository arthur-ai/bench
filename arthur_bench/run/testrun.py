import uuid
from arthur_bench.models.models import CreateRunRequest
from arthur_bench.client.bench_client import BenchClient


class TestRun(CreateRunRequest):
    test_suite_id: uuid.UUID
    client: BenchClient # type: ignore

    class Config:
        arbitrary_types_allowed = True


    def save(self):
        """Save a test run to local file system."""
        return self.client.create_new_test_run(test_suite_id=str(self.test_suite_id), 
                                               json_body=CreateRunRequest(**self.dict()))