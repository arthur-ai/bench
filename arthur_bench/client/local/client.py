import os
import getpass
import numpy as np
import glob
import json
from datetime import datetime
from math import ceil
from typing import Optional, Union, List, Dict, Any
from dataclasses import dataclass
import uuid
from pathlib import Path
from collections import defaultdict
from arthur_bench.client.bench_client import BenchClient
from arthur_bench.exceptions import NotFoundError, ArthurError, UserValueError
from arthur_bench.models.models import (
    CreateRunRequest,
    CreateRunResponse,
    PaginatedRun,
    PaginatedRuns,
    PaginatedTestSuite,
    PaginatedTestSuites,
    TestSuiteRequest,
    TestSuiteSummary,
    TestSuiteMetadata,
    TestRunMetadata,
    SummaryItem,
    HistogramItem,
    CategoricalHistogramItem,
    TestCaseRequest,
    TestCaseResponse,
    RunResult,
    ScoringMethod,
    ScorerOutputType,
    PaginationSuiteSortEnum,
    PaginationRunSortEnum,
    PaginationSortEnum,
    CommonSortEnum,
    TestCaseSortEnum,
    TestRunSortEnum,
    TestSuiteSortEnum,
)

from arthur_bench.utils.loaders import load_suite_from_json, get_file_extension

BENCH_FILE_DIR_KEY = "BENCH_FILE_DIR"
DEFAULT_BENCH_FILE_DIR = Path(os.getcwd()) / "bench_runs"

SUITE_INDEX_FILE = "suite_id_to_name.json"
RUN_INDEX_FILE = "run_id_to_name.json"

DEFAULT_PAGE_SIZE = 5

NUM_BINS = 20

SORT_QUERY_TO_FUNC = {
    TestSuiteSortEnum.LAST_RUNTIME_ASC: lambda x: (
        x.last_run_time if x.last_run_time is not None else x.created_at
    ),
    CommonSortEnum.NAME_ASC: lambda x: x.name,
    CommonSortEnum.CREATED_AT_ASC: lambda x: x.created_at,
    TestRunSortEnum.AVG_SCORE_ASC: lambda x: x.avg_score,
    TestSuiteSortEnum.LAST_RUNTIME_DESC: lambda x: (
        x.last_run_time if x.last_run_time is not None else x.created_at
    ),
    CommonSortEnum.NAME_DESC: lambda x: x.name,
    CommonSortEnum.CREATED_AT_DESC: lambda x: x.created_at,
    TestRunSortEnum.AVG_SCORE_DESC: lambda x: x.avg_score,
    TestCaseSortEnum.SCORE_ASC: lambda x: x.score,
    TestCaseSortEnum.SCORE_DESC: lambda x: x.score,
}


def _bench_root_dir() -> Path:
    return Path(os.environ.get(BENCH_FILE_DIR_KEY, DEFAULT_BENCH_FILE_DIR))


def _initialize_metadata() -> Dict[str, Any]:
    timestamp = datetime.now().isoformat()
    return {
        "created_at": timestamp,
        "created_by": getpass.getuser(),
        "updated_at": timestamp,
    }


def _load_suite_with_optional_id(
    filepath: Union[str, os.PathLike]
) -> Optional[PaginatedTestSuite]:
    if get_file_extension(filepath) != ".json":
        raise UserValueError("filepath must be json file")
    suite = json.load(open(filepath))
    if "id" in suite:
        return PaginatedTestSuite.parse_obj(suite)
    return None


def _summarize_run(
    run: PaginatedRun, scoring_method: ScoringMethod, num_bins=NUM_BINS
) -> SummaryItem:
    """
    Compute aggregate statistics for a run. If scorer defined categories, categorical
    histogram will be returned, otherwise continuous values will be grouped into 20
    bins.
    """
    scores = np.array([o.score_result.score for o in run.test_cases])
    avg_score = np.mean(scores).item()
    histogram: List[Union[HistogramItem, CategoricalHistogramItem]] = []

    if scoring_method.output_type == ScorerOutputType.Categorical:
        # count values in results
        value_counts: defaultdict[str, int] = defaultdict(int)
        for result in run.test_cases:
            # we validate at score time that categorical scorers specify non-null
            # categories
            value_counts[result.score_result.category.name] += 1  # type: ignore

        categories = scoring_method.categories
        # we validate that all categorical scoring methods have non null categories
        for cat in categories:  # type: ignore
            cat_hist_item = CategoricalHistogramItem(
                count=value_counts[cat.name], category=cat
            )
            histogram.append(cat_hist_item)

    else:
        hist, bin_edges = np.histogram(
            scores, bins=num_bins, range=(0, max(1, np.max(scores)))
        )
        for i in range(len(hist)):
            hist_item = HistogramItem(
                count=hist[i], low=bin_edges[i], high=bin_edges[i + 1]
            )
            histogram.append(hist_item)
    return SummaryItem(
        id=run.id,
        name=run.name,
        avg_score=avg_score,
        histogram=histogram,
    )


@dataclass
class PageInfo:
    sorted_pages: List
    start: int
    end: int
    page: int
    page_size: int
    total_pages: int
    total_count: int


def _paginate(
    objs: List, page: int, page_size: int, sort_key: Optional[PaginationSortEnum] = None
) -> PageInfo:
    """Paginate sorted files and return iteration indices and page info"""
    if sort_key is not None:
        desc = sort_key[0] == "-"
        sorted_pages = sorted(objs, key=SORT_QUERY_TO_FUNC.get(sort_key), reverse=desc)
    else:
        sorted_pages = objs
    offset = (page - 1) * page_size
    return PageInfo(
        sorted_pages=sorted_pages,
        start=offset,
        end=min(offset + page_size, len(objs)),
        page=page,
        page_size=page_size,
        total_count=len(objs),
        total_pages=max(1, ceil(len(objs) / page_size)),
    )


class LocalBenchClient(BenchClient):
    """
    Client for managing local file system test suites and runs
    """

    def __init__(self, root_dir: Optional[Union[str, Path]] = None):
        if root_dir is None:
            root_dir = _bench_root_dir()

        # if root dir does not exist, create:
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)

        self.root_dir = Path(root_dir)
        self._write_suite_index()

    def _test_suite_dir(self, test_suite_name: str):
        return Path(self.root_dir) / test_suite_name

    def _create_test_suite_dir(self, test_suite_name: str) -> Path:
        test_suite_dir = self._test_suite_dir(test_suite_name)
        if test_suite_dir.is_dir():
            raise UserValueError(f"test_suite {test_suite_name} already exists")
        os.mkdir(test_suite_dir)
        return test_suite_dir

    def _create_run_dir(self, test_suite_name: str, run_name: str) -> Path:
        run_dir = self._test_suite_dir(test_suite_name) / run_name
        if os.path.exists(run_dir):
            raise UserValueError(f"run {run_name} already exists")
        os.mkdir(run_dir)
        return run_dir

    def _get_suite_name_from_id(self, id: str) -> Optional[str]:
        suite_index = json.load(open(self.root_dir / SUITE_INDEX_FILE))
        if id not in suite_index:
            return None
        return suite_index[id]

    def _get_run_name_from_id(self, test_suite_name: str, id: str) -> Optional[str]:
        run_index = json.load(open(self.root_dir / test_suite_name / RUN_INDEX_FILE))
        if id not in run_index:
            return None
        return run_index[id]

    def _create_test_case_with_id(self, test_case: TestCaseRequest) -> TestCaseResponse:
        return TestCaseResponse(
            id=uuid.uuid4(),
            input=test_case.input,
            reference_output=test_case.reference_output,
        )

    def _update_suite_run_time(self, test_suite_name: str, runtime: datetime):
        suite_file = self.root_dir / test_suite_name / "suite.json"
        suite = PaginatedTestSuite.parse_file(suite_file)
        suite.last_run_time = runtime
        suite.num_runs += 1
        suite_file.write_text(suite.json())

    def _write_suite_index(self):
        suite_index_path = self.root_dir / SUITE_INDEX_FILE
        if suite_index_path.is_file():
            return
        json.dump({}, open(suite_index_path, "w"))
        return None

    def _write_run_index(self, test_suite: str):
        run_index_path = self.root_dir / test_suite / RUN_INDEX_FILE
        if run_index_path.is_file():
            return
        json.dump({}, open(run_index_path, "w"))
        return None

    @staticmethod
    def _update_index(filepath: Path, id: uuid.UUID, name: str):
        suite_index = json.load(open(filepath))
        suite_index[str(id)] = name
        json.dump(suite_index, open(filepath, "w"))

    def _update_suite_index(self, id: uuid.UUID, name: str):
        suite_index_path = self.root_dir / SUITE_INDEX_FILE
        LocalBenchClient._update_index(suite_index_path, id, name)

    def _update_run_index(self, test_suite_name: str, id: uuid.UUID, name: str):
        run_index_path = self.root_dir / test_suite_name / RUN_INDEX_FILE
        LocalBenchClient._update_index(run_index_path, id, name)

    def get_test_suite(
        self, test_suite_id: str, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedTestSuite:
        suite_index = json.load(open(self.root_dir / SUITE_INDEX_FILE))
        if test_suite_id not in suite_index:
            raise NotFoundError(f"no test suite with id: {test_suite_id}")
        else:
            suite_file = self.root_dir / suite_index[test_suite_id] / "suite.json"
            suite = PaginatedTestSuite.parse_file(suite_file)
            pagination = _paginate(suite.test_cases, page, page_size)
            return PaginatedTestSuite(
                id=uuid.UUID(test_suite_id),
                name=suite.name,
                scoring_method=suite.scoring_method,
                test_cases=pagination.sorted_pages[pagination.start : pagination.end],
                created_at=suite.created_at,
                updated_at=suite.updated_at,
                last_run_time=suite.last_run_time,
                num_runs=suite.num_runs,
                page=pagination.page,
                page_size=pagination.page_size,
                total_count=pagination.total_count,
                total_pages=pagination.total_pages,
            )

    def get_test_suites(
        self,
        name: Optional[str] = None,
        sort: PaginationSuiteSortEnum = TestSuiteSortEnum.LAST_RUNTIME_ASC,
        scoring_method: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> PaginatedTestSuites:
        # name uniqueness
        if name is not None:
            test_suite_dir = self.root_dir / name
            if test_suite_dir.is_dir():
                suite = _load_suite_with_optional_id(test_suite_dir / "suite.json")
                if suite is None:
                    suite = self.get_test_suite_by_name(name)
                return PaginatedTestSuites(
                    test_suites=[
                        TestSuiteMetadata(
                            id=suite.id,
                            name=suite.name,
                            scoring_method=suite.scoring_method,
                            description=suite.description,
                            created_at=suite.created_at,
                            updated_at=suite.updated_at,
                            last_run_time=suite.last_run_time,
                        )
                    ],
                    page=1,
                    page_size=page_size,
                    total_pages=1,
                    total_count=1,
                )
            else:
                return PaginatedTestSuites(
                    test_suites=[],
                    page=1,
                    page_size=page_size,
                    total_pages=1,
                    total_count=0,
                )

        suites: List[TestSuiteMetadata] = []
        suite_files = glob.glob(f"{self.root_dir}/*/suite.json")
        for f in suite_files:
            suite = _load_suite_with_optional_id(f)
            if suite is None:
                suite = self.get_test_suite_by_name(f.split("/")[-2])
            if scoring_method is None or suite.scoring_method.name in scoring_method:
                suites.append(
                    TestSuiteMetadata(
                        id=suite.id,
                        name=suite.name,
                        scoring_method=suite.scoring_method,
                        description=suite.description,
                        created_at=suite.created_at,
                        updated_at=suite.updated_at,
                        last_run_time=suite.last_run_time,
                    )
                )

        paginate = _paginate(suites, page=page, page_size=page_size, sort_key=sort)
        return PaginatedTestSuites(
            test_suites=paginate.sorted_pages[paginate.start : paginate.end],
            page=paginate.page,
            page_size=paginate.page_size,
            total_pages=paginate.total_pages,
            total_count=paginate.total_count,
        )

    def create_test_suite(self, json_body: TestSuiteRequest) -> PaginatedTestSuite:
        test_suite_dir = self._create_test_suite_dir(json_body.name)
        suite_file = test_suite_dir / "suite.json"

        test_suite_id = uuid.uuid4()
        self._update_suite_index(test_suite_id, json_body.name)
        self._write_run_index(json_body.name)

        resp = PaginatedTestSuite(
            id=test_suite_id,
            name=json_body.name,
            test_cases=[
                self._create_test_case_with_id(test_case)
                for test_case in json_body.test_cases
            ],
            description=json_body.description,
            scoring_method=json_body.scoring_method,
            **_initialize_metadata(),
        )

        suite_file.write_text(resp.json())
        return resp

    def create_new_test_run(
        self, test_suite_id: str, json_body: CreateRunRequest
    ) -> CreateRunResponse:
        test_suite_name = self._get_suite_name_from_id(test_suite_id)
        if test_suite_name is None:
            raise NotFoundError(f"no test suite with id {test_suite_id} ")

        run_id = uuid.uuid4()
        resp = PaginatedRun(
            id=run_id,
            test_suite_id=uuid.UUID(test_suite_id),
            **_initialize_metadata(),
            **json_body.dict(),
        )

        run_dir = self._create_run_dir(test_suite_name, json_body.name)
        run_file = run_dir / "run.json"
        run_file.write_text(resp.json())
        self._update_run_index(test_suite_name, run_id, json_body.name)
        self._update_suite_run_time(
            test_suite_name=test_suite_name, runtime=resp.created_at
        )
        return CreateRunResponse(id=resp.id)

    def get_runs_for_test_suite(
        self,
        test_suite_id: str,
        sort: PaginationRunSortEnum = CommonSortEnum.CREATED_AT_ASC,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> PaginatedRuns:
        test_suite_name = self._get_suite_name_from_id(test_suite_id)
        if test_suite_name is None:
            raise NotFoundError(f"no test suite with id: {test_suite_id}")

        runs = []
        run_files = glob.glob(f"{self.root_dir}/{test_suite_name}/*/run.json")
        for f in run_files:
            run_obj = PaginatedRun.parse_file(f)
            avg_score = np.mean([o.score for o in run_obj.test_cases])
            run_resp = TestRunMetadata(**run_obj.dict(), avg_score=float(avg_score))
            runs.append(run_resp)

        pagination = _paginate(runs, page, page_size, sort_key=sort)

        return PaginatedRuns(
            test_runs=pagination.sorted_pages[pagination.start : pagination.end],
            page_size=pagination.page_size,
            page=pagination.page,
            total_pages=pagination.total_pages,
            total_count=pagination.total_count,
        )

    def get_summary_statistics(
        self,
        test_suite_id: str,
        run_ids: Optional[list[str]] = None,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> TestSuiteSummary:
        test_suite_name = self._get_suite_name_from_id(test_suite_id)
        if test_suite_name is None:
            raise NotFoundError(f"no test suite with id {test_suite_id}")

        suite = self.get_suite_if_exists(test_suite_name)
        if suite is None:
            raise NotFoundError(f"no test suite with id {test_suite_id}")

        runs: list[SummaryItem] = []
        run_files = glob.glob(f"{self.root_dir}/{test_suite_name}/*/run.json")

        if run_ids:
            run_name_to_file_dict = {file.split("/")[-2]: file for file in run_files}
            run_names = [
                self._get_run_name_from_id(test_suite_name, id) for id in run_ids
            ]
            filtered_run_files = {
                k: run_name_to_file_dict[k]
                for k in run_names
                if k in run_name_to_file_dict
            }
            run_files = list(filtered_run_files.values())

        for f in run_files:
            run_obj = PaginatedRun.parse_file(f)
            runs.append(
                _summarize_run(run=run_obj, scoring_method=suite.scoring_method)
            )

        pagination = _paginate(
            runs, page, page_size, sort_key=TestRunSortEnum.AVG_SCORE_ASC
        )
        paginated_summary = TestSuiteSummary(
            summary=runs,
            categorical=suite.scoring_method.output_type
            == ScorerOutputType.Categorical,
            num_test_cases=len(suite.test_cases),
            page_size=pagination.page_size,
            page=pagination.page,
            total_pages=pagination.total_pages,
            total_count=pagination.total_count,
        )

        return paginated_summary

    def get_test_run(
        self,
        test_suite_id: str,
        test_run_id: str,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort: Optional[TestCaseSortEnum] = None,
    ) -> PaginatedRun:
        test_suite_name = self._get_suite_name_from_id(test_suite_id)
        if test_suite_name is None:
            raise NotFoundError(f"test suite with id: {test_suite_id} does not exist")

        run_name = self._get_run_name_from_id(test_suite_name, test_run_id)
        if run_name is None:
            raise NotFoundError(f"test run with id: {test_run_id} does not exist")

        run_data = PaginatedRun.parse_file(
            self.root_dir / test_suite_name / run_name / "run.json"
        )
        suite_data = PaginatedTestSuite.parse_file(
            self.root_dir / test_suite_name / "suite.json"
        )
        run_results = []
        for i, test_case in enumerate(run_data.test_cases):
            run_result = RunResult(
                id=test_case.id,
                output=test_case.output,
                score=test_case.score,
                score_result=test_case.score_result,
                input=suite_data.test_cases[i].input,
                reference_output=suite_data.test_cases[i].reference_output,
            )
            run_results.append(run_result)

        pagination = _paginate(run_results, page, page_size, sort_key=sort)
        return PaginatedRun(
            id=uuid.UUID(test_run_id),
            name=run_name,
            created_at=run_data.created_at,
            updated_at=run_data.created_at,
            test_case_runs=pagination.sorted_pages[pagination.start : pagination.end],
            test_suite_id=uuid.UUID(test_suite_id),
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=pagination.total_pages,
            total_count=pagination.total_count,
        )

    def delete_test_suite(self, test_suite_id: str):
        # TODO
        return ArthurError("delete test suite is not supported in local mode yet")

    def delete_test_run(self, test_suite_id: str, test_run_id: str):
        # TODO:
        return ArthurError("delete test run is not supported in local mode yet")

    def get_test_suite_by_name(self, test_suite_name: str) -> PaginatedTestSuite:
        """
        Additional getter to maintain backwards compatibility with non-identified
        local files
        """
        suite_file = self.root_dir / test_suite_name / "suite.json"
        suite = load_suite_from_json(suite_file)

        # override file with index
        id_ = uuid.uuid4()
        resp = PaginatedTestSuite(id=id_, **suite.dict())
        suite_file.write_text(resp.json())
        self._update_suite_index(id_, test_suite_name)
        self._write_run_index(test_suite_name)

        return resp
