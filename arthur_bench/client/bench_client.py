from typing import Optional, TypeVar
from abc import ABC, abstractmethod

from arthur_bench.models.models import (
    PaginatedTestSuites,
    CreateRunResponse,
    CreateRunRequest,
    PaginatedRuns,
    PaginatedRun,
    TestSuiteRequest,
    PaginatedTestSuite,
    TestSuiteSummary,
)

TBenchClient = TypeVar("TBenchClient", bound="BenchClient")


class BenchClient(ABC):

    @abstractmethod
    def get_test_suites(
        self,
        name: Optional[str] = None,
        sort: Optional[str] = None,
        scoring_method: Optional[str] = None,
        page: int = 1,
        page_size: Optional[int] = None
    ) -> PaginatedTestSuites:
        raise NotImplementedError
    
    @abstractmethod
    def create_test_suite(self, json_body: TestSuiteRequest) -> PaginatedTestSuite:
        raise NotImplementedError
    
    @abstractmethod
    def get_test_suite(
        self, 
        test_suite_id: str,
        page: int = 1,
        page_size: Optional[int] = None) -> PaginatedTestSuite:
        raise NotImplementedError
    
    @abstractmethod
    def get_runs_for_test_suite(
        self, 
        test_suite_id: str, 
        sort: Optional[str] = None,
        page: int = 1,
        page_size: Optional[int] = None
    ) -> PaginatedRuns:
        raise NotImplementedError
    
    @abstractmethod
    def create_new_test_run(
        self, test_suite_id: str, json_body: CreateRunRequest
    ) -> CreateRunResponse:
        raise NotImplementedError
    
    @abstractmethod
    def get_test_run(
        self,
        test_suite_id: str,
        test_run_id: str,
        page: int = 1,
        page_size: Optional[int] = None,
        sort: Optional[bool] = None,
    ) -> PaginatedRun:
        raise NotImplementedError
    
    @abstractmethod
    def get_summary_statistics(
        self,
        test_suite_id: str,
        run_id: Optional[str] = None,
        page: int = 1,
        page_size: Optional[int] = None,
    ) -> TestSuiteSummary:
        raise NotImplementedError
    
    @abstractmethod
    def delete_test_suite(self, test_suite_id: str):
        raise NotImplementedError
    
    @abstractmethod
    def delete_test_run(self, test_suite_id: str, test_run_id: str):
        raise NotImplementedError
