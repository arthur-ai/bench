import json
from typing import Optional
import uuid
from pathlib import Path
from arthur_bench.client.bench_client import BenchClient
from arthur_bench.client.exceptions import NotFoundError
from arthur_bench.models.models import CreateRunRequest, CreateRunResponse, PaginatedGetRunResponse, PaginatedGetRunsForTestSuiteResponse, PaginatedGetTestSuiteResponse, PaginatedGetTestSuitesResponse, TestSuiteRequest, TestSuiteResponse, TestSuiteSummaryResponse
from arthur_bench.run.utils import _bench_root_dir, load_suite_from_json, _create_test_suite_dir, _create_run_dir

SUITE_INDEX_FILE = 'suite_id_to_name.json'
RUN_INDEX_FILE = 'run_id_to_name.json'

def _write_suite_index(root_dir: Path):
    suite_index_path = root_dir / SUITE_INDEX_FILE
    if suite_index_path.is_file():
        return
    json.dump({}, open(suite_index_path, "w"))
    return None


def _write_run_index(root_dir: Path, test_suite: str):
    run_index_path = root_dir / test_suite / RUN_INDEX_FILE
    if run_index_path.is_file():
        return
    json.dump({}, open(run_index_path, "w"))
    return None


class LocalBenchClient(BenchClient):
    """
    Client for managing local file system test suites and runs
    """
    def __init__(self):
        self.root_dir = _bench_root_dir()
        _write_suite_index(self.root_dir)

    def _get_suite_name_from_id(self, id: str) -> str:
        suite_index = json.load(open(self.root_dir / SUITE_INDEX_FILE))
        if id not in suite_index:
            return None
        return suite_index[id]
    
    @staticmethod
    def _update_index(filepath: Path, id: uuid, name: str):
        suite_index = json.load(open(filepath))
        suite_index[str(id)] = name
        json.dump(suite_index, open(filepath, "w"))

    def _update_suite_index(self, id: uuid, name: str):
        suite_index_path = self.root_dir / SUITE_INDEX_FILE
        LocalBenchClient._update_index(suite_index_path, id, name)

    def _update_run_index(self, test_suite_name: str, id: uuid, name: str):
        run_index_path = self.root_dir / test_suite_name / RUN_INDEX_FILE
        LocalBenchClient._update_index(run_index_path, id, name)

    def get_test_suite(self, test_suite_id: str, page: int = 1, page_size: Optional[int] = None) -> PaginatedGetTestSuiteResponse:
        suite_index = json.load(open(self.root_dir / SUITE_INDEX_FILE))
        if test_suite_id not in suite_index:
            return PaginatedGetTestSuiteResponse()
        else:
            suite_file = self.root_dir / suite_index[test_suite_id] / "suite.json"
            suite = load_suite_from_json(suite_file)
            # TODO: pagination
            return PaginatedGetTestSuiteResponse(**suite)
        
    def get_test_suites(self, name: Optional[str] = None, sort: Optional[str] = None, scoring_method: Optional[str] = None, page: int = 1, page_size: Optional[int] = None) -> PaginatedGetTestSuitesResponse:
        if name is not None:
            test_suite_dir = self.root_dir / name
            if test_suite_dir.is_dir():
                return load_suite_from_json(test_suite_dir / "suite.json")
            else:
                # TODO: pagination
                return PaginatedGetTestSuitesResponse(test_suites=[])
        # TODO: finish this method
        return PaginatedGetTestSuitesResponse(test_suites=[])
        
    def create_test_suite(self, json_body: TestSuiteRequest) -> TestSuiteResponse:
        test_suite_dir = _create_test_suite_dir(json_body.name)
        suite_file = test_suite_dir / "suite.json"

        test_suite_id = uuid.uuid4()
        self._update_suite_index(test_suite_id, json_body.name)
        _write_run_index(self.root_dir, json_body.name)

        suite_file.write_text(json_body.json())
        return TestSuiteResponse(id=test_suite_id,
                                 **json_body.dict())
    
    def create_new_test_run(self, test_suite_id: str, json_body: CreateRunRequest) -> CreateRunResponse:
        test_suite_name = self._get_suite_name_from_id(test_suite_id)
        if test_suite_name is None:
            raise NotFoundError()
        run_dir = _create_run_dir(test_suite_name, json_body.name)

        run_file = run_dir / 'run.json'
        run_file.write_text(json_body.json())

        run_id = uuid.uuid4()
        self._update_run_index(test_suite_name, run_id, json_body.name)
        return CreateRunResponse(id=run_id)
    
    def get_runs_for_test_suite(self, test_suite_id: str, sort: Optional[str] = None, page: int = 1, page_size: Optional[int] = None) -> PaginatedGetRunsForTestSuiteResponse:
        # TODO:
        return super().get_runs_for_test_suite(test_suite_id, sort, page, page_size)
    
    def get_summary_statistics(self, test_suite_id: str, run_id: Optional[str] = None, page: int = 1, page_size: Optional[int] = None) -> TestSuiteSummaryResponse:
        # TODO: 
        return super().get_summary_statistics(test_suite_id, run_id, page, page_size)
    
    def get_test_run(self, test_suite_id: str, test_run_id: str, page: int = 1, page_size: Optional[int] = None, sort: Optional[bool] = None) -> PaginatedGetRunResponse:
        # TODO:
        return super().get_test_run(test_suite_id, test_run_id, page, page_size, sort)
    
    def delete_test_suite(self, test_suite_id: str):
        # TODO
        return super().delete_test_suite(test_suite_id)
    
    def delete_test_run(self, test_suite_id: str, test_run_id: str):
        # TODO:
        return super().delete_test_run(test_suite_id, test_run_id)
