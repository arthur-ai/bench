import dataclasses
import glob
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, List

from arthur_bench.client.fs.abc_fs_client import ABCFSClient
from arthur_bench.exceptions import UserValueError, NotFoundError
from arthur_bench.models.models import PaginatedTestSuite, PaginatedRun
from arthur_bench.utils.loaders import load_suite_from_json, get_file_extension


@dataclasses.dataclass(frozen=True)
class LocalFSClientConfig:
    root_dir: Optional[Path]


SUITE_INDEX_FILE = "suite_id_to_name.json"
RUN_INDEX_FILE = "run_id_to_name.json"


def _bench_root_dir() -> Path:
    return Path(os.environ.get("BENCH_FILE_DIR", Path(os.getcwd()) / "bench_runs"))


class LocalFSClient(ABCFSClient):

    def __init__(self, config: LocalFSClientConfig):
        super().__init__(config)
        if config.root_dir is None:
            root_dir = _bench_root_dir()
        else:
            root_dir = config.root_dir

        if not os.path.exists(root_dir):
            os.mkdir(root_dir)

        self.root_dir = Path(root_dir)
        self.write_suite_index()

    def get_test_suite_dir(self, test_suite_name: str) -> Path:
        return Path(self.root_dir) / test_suite_name

    def create_test_suite_dur(self, test_suite_name: str) -> Path:
        test_suite_dir = self.get_test_suite_dir(test_suite_name)
        if test_suite_dir.is_dir():
            raise UserValueError(f"test_suite {test_suite_name} already exists")
        os.mkdir(test_suite_dir)
        return test_suite_dir

    def create_run_dir(self, test_suite_name: str, run_name: str) -> Path:
        run_dir = self.get_test_suite_dir(test_suite_name) / run_name
        if os.path.exists(run_dir):
            raise UserValueError(f"run {run_name} already exists")
        os.mkdir(run_dir)
        return run_dir

    def get_suite_name_from_id(self, id: str) -> Optional[str]:
        suite_index = json.load(open(self.root_dir / SUITE_INDEX_FILE))
        if id not in suite_index:
            return None
        return suite_index[id]

    def get_run_name_from_id(self, test_suite_name: str, id: str) -> Optional[str]:
        run_index = json.load(open(self.root_dir / test_suite_name / RUN_INDEX_FILE))
        if id not in run_index:
            return None
        return run_index[id]

    def update_suite_run_time(self, test_suite_name: str, runtime: datetime) -> None:
        suite_file = self.root_dir / test_suite_name / "suite.json"
        suite = PaginatedTestSuite.parse_file(suite_file)
        suite.last_run_time = runtime
        suite.num_runs += 1
        suite_file.write_text(suite.json())

    def write_suite_index(self) -> None:
        suite_index_path = self.root_dir / SUITE_INDEX_FILE
        if suite_index_path.is_file():
            return
        json.dump({}, open(suite_index_path, "w"))
        return None

    def write_run_index(self, test_suite: str) -> None:
        run_index_path = self.root_dir / test_suite / RUN_INDEX_FILE
        if run_index_path.is_file():
            return
        json.dump({}, open(run_index_path, "w"))
        return None

    @staticmethod
    def update_index(filepath: Path, id: uuid.UUID, name: str) -> None:
        suite_index = json.load(open(filepath))
        suite_index[str(id)] = name
        json.dump(suite_index, open(filepath, "w"))

    def update_suite_index(self, id: uuid.UUID, name: str) -> None:
        suite_index_path = self.root_dir / SUITE_INDEX_FILE
        LocalFSClient.update_index(suite_index_path, id, name)

    def update_run_index(self, test_suite_name: str, id: uuid.UUID, name: str) -> None:
        run_index_path = self.root_dir / test_suite_name / RUN_INDEX_FILE
        LocalFSClient.update_index(run_index_path, id, name)

    def get_test_suite_by_name(self, test_suite_name: str) -> PaginatedTestSuite:
        suite_file = self.root_dir / test_suite_name / "suite.json"
        suite = load_suite_from_json(suite_file)

        # override file with index
        id_ = uuid.uuid4()
        resp = PaginatedTestSuite(id=id_, **suite.dict())
        suite_file.write_text(resp.json())
        self.update_suite_index(id_, test_suite_name)
        self.write_run_index(test_suite_name)

        return resp

    @staticmethod
    def load_suite_with_optional_id(
        filepath: Union[str, os.PathLike]
    ) -> Optional[PaginatedTestSuite]:
        if get_file_extension(filepath) != ".json":
            raise UserValueError("filepath must be json file")
        suite = json.load(open(filepath))
        if "id" in suite:
            return PaginatedTestSuite.parse_obj(suite)
        return None

    def get_suite_files(self) -> List[str]:
        return glob.glob(f"{self.root_dir}/*/suite.json")

    def get_run_files(self, test_suite_name: str) -> List[str]:
        return glob.glob(f"{self.root_dir}/{test_suite_name}/*/run.json")

    def parse_paginated_test_suite(self, id: str) -> PaginatedTestSuite:
        suite_name = self.get_suite_name_from_id(id)
        if not suite_name:
            raise NotFoundError(f"no test suite with id: {id}")

        suite_file = self.root_dir / suite_name / "suite.json"
        return PaginatedTestSuite.parse_file(suite_file)

    def parse_paginated_test_run(
        self, test_suite_id: str, run_name: str
    ) -> PaginatedRun:
        suite_name = self.get_suite_name_from_id(test_suite_id)
        if not suite_name:
            raise NotFoundError(f"no test suite with id: {test_suite_id}")

        return PaginatedRun.parse_file(
            self.root_dir / suite_name / run_name / "run.json"
        )

    def write_suite_file(self, suite_dir: Path, test_suite: PaginatedTestSuite) -> None:
        suite_file = suite_dir / "suite.json"
        suite_file.write_text(test_suite.json())

    def write_run_file(self, run_dir: Path, test_run: PaginatedRun) -> None:
        run_file = run_dir / "run.json"
        run_file.write_text(test_run.json())
