from typing import Optional
from abc import ABC, abstractmethod

from arthur_bench.models.models import (
    PaginatedGetTestSuitesResponse,
    CreateRunResponse,
    CreateRunRequest,
    PaginatedGetRunsForTestSuiteResponse,
    PaginatedGetRunResponse,
    TestSuiteResponse,
    TestSuiteRequest,
    PaginatedGetTestSuiteResponse,
    TestSuiteSummaryResponse,
)

class BenchClient(ABC):

    @abstractmethod
    def get_test_suites(
        self,
        name: Optional[str] = None,
        sort: Optional[str] = None,
        scoring_method: Optional[str] = None,
        page: int = 1,
        page_size: Optional[int] = None
    ) -> PaginatedGetTestSuitesResponse:
        raise NotImplementedError
    
    @abstractmethod
    def create_test_suite(self, json_body: TestSuiteRequest) -> TestSuiteResponse:
        raise NotImplementedError
    
    @abstractmethod
    def get_test_suite(
        self, 
        test_suite_id: str,
        page: int = 1,
        page_size: Optional[int] = None) -> PaginatedGetTestSuiteResponse:
        raise NotImplementedError
    
    @abstractmethod
    def get_runs_for_test_suite(
        self, 
        test_suite_id: str, 
        sort: Optional[str] = None,
        page: int = 1,
        page_size: Optional[int] = None
    ) -> PaginatedGetRunsForTestSuiteResponse:
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
    ) -> PaginatedGetRunResponse:
        raise NotImplementedError
    
    @abstractmethod
    def get_summary_statistics(
        self,
        test_suite_id: str,
        run_id: Optional[str] = None,
        page: int = 1,
        page_size: Optional[int] = None,
    ) -> TestSuiteSummaryResponse:
        raise NotImplementedError
    
    @abstractmethod
    def delete_test_suite(self, test_suite_id: str):
        raise NotImplementedError
    
    @abstractmethod
    def delete_test_run(self, test_suite_id: str, test_run_id: str):
        raise NotImplementedError
