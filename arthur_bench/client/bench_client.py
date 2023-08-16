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

from arthur_bench.client.exceptions import ArthurInternalError

TBenchClient = TypeVar("TBenchClient", bound="BenchClient")


class BenchClient(ABC):
    @abstractmethod
    def get_test_suites(
        self,
        name: Optional[str] = None,
        sort: Optional[str] = None,
        scoring_method: Optional[str] = None,
        page: int = 1,
        page_size: int = 5,
    ) -> PaginatedTestSuites:
        raise NotImplementedError

    @abstractmethod
    def create_test_suite(self, json_body: TestSuiteRequest) -> PaginatedTestSuite:
        raise NotImplementedError

    @abstractmethod
    def get_test_suite(
        self, test_suite_id: str, page: int = 1, page_size: int = 5
    ) -> PaginatedTestSuite:
        raise NotImplementedError

    @abstractmethod
    def get_runs_for_test_suite(
        self,
        test_suite_id: str,
        sort: Optional[str] = None,
        page: int = 1,
        page_size: int = 5,
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
        page_size: int = 5,
        sort: Optional[bool] = None,
    ) -> PaginatedRun:
        raise NotImplementedError

    @abstractmethod
    def get_summary_statistics(
        self,
        test_suite_id: str,
        run_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 5,
    ) -> TestSuiteSummary:
        raise NotImplementedError

    @abstractmethod
    def delete_test_suite(self, test_suite_id: str):
        raise NotImplementedError

    @abstractmethod
    def delete_test_run(self, test_suite_id: str, test_run_id: str):
        raise NotImplementedError

    def get_suite_if_exists(self, name: str) -> Optional[PaginatedTestSuite]:
        """
        Get a full test suite with name if it exists.

        :param client: BenchClient object for fetching test suite data
        :return: complete test suite with all test cases joined,
            or None if no suite with name exists
        :raises ArthurInternalError: if using a client that does not support pagination
        """
        test_suite_resp = self.get_test_suites(name=name)
        if len(test_suite_resp.test_suites) > 0:
            # we enforce name validation, so there should ever only be one
            query_params = {"page_size": 100}

            suite = self.get_test_suite(
                str(test_suite_resp.test_suites[0].id), **query_params
            )

            current_page: int
            total_pages: int
            if suite.page is None or suite.total_pages is None:
                raise ArthurInternalError("expected paginated response")

            current_page = suite.page + 1
            total_pages = suite.total_pages
            while current_page <= total_pages:
                query_params["page"] = current_page
                suite_next_page = self.get_test_suite(
                    str(test_suite_resp.test_suites[0].id), **query_params
                )

                suite.test_cases.extend(suite_next_page.test_cases)

                if suite_next_page.page is None or suite_next_page.total_pages is None:
                    raise ArthurInternalError("expected paginated response")
                total_pages = suite_next_page.total_pages
                current_page = suite_next_page.page + 1
            return suite
        return None

    def check_run_exists(self, suite_id: str, run_name: str) -> bool:
        """
        Check if run with given name if it exists for suite with id suite_id

        :param client: BenchClient object for fetching test suite data
        :param suite_id: the id of the test suite to check run names
        :param run_name: the test run name to check for
        :return: True if run with name is found, False otherwise
        :raises ArthurInternalError: if using a client that does not support pagination
        """

        page_size = 100
        current_page = 1
        total_pages = 1
        page = 1

        while current_page <= total_pages:
            runs = self.get_runs_for_test_suite(
                suite_id, page=page, page_size=page_size
            )
            for run_metadata in runs.test_runs:
                if run_metadata.name == run_name:
                    return True
            if runs.page is None or runs.total_pages is None:
                raise ArthurInternalError("expected paginated response")
            total_pages = runs.total_pages
            current_page = runs.page + 1
        return False
