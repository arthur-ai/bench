from typing import Optional, Dict, cast
from http import HTTPStatus
from requests.cookies import RequestsCookieJar

# import http client
from arthur_bench.client.http.requests import HTTPClient

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


PATH_PREFIX = "/api/v3"


class ArthurBenchClient:
    """
    A Python client to interact with the Arthur Bench API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurBenchClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def get_test_suites(
        self,
        name: Optional[str] = None,
        sort: Optional[str] = None,
        scoring_method: Optional[str] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = None
    ) -> PaginatedGetTestSuitesResponse:
        """
                Gets test suites

                Sort by latest run by default.
        If `name` query parameter is provided, filter on test suite name.

                :param name:
                :param sort:
                :param scoring_method:
        """

        params = {}
        if name is not None:
            params["name"] = name
        if sort is not None:
            params["sort"] = sort
        if scoring_method is not None:
            params["scoring_method"] = scoring_method
        if page is not None:
            params["page"] = page # type: ignore
        if page_size is not None:
            params["page_size"] = page_size # type: ignore

        parsed_resp = cast(Dict, self.http_client.get(
            f"/bench/test_suites", params=params, validation_response_code=HTTPStatus.OK
        ))
        return PaginatedGetTestSuitesResponse(**parsed_resp)

    def create_test_suite(self, json_body: TestSuiteRequest) -> TestSuiteResponse:
        """
        Creates a new test suite from reference data using specified scoring_method for scoring

        :param json_body:
        """

        parsed_resp = cast(Dict, self.http_client.post(
            f"/bench/test_suites",
            json=json_body.dict(exclude={'created_at', 'created_by', 'bench_version'}),
            validation_response_code=HTTPStatus.CREATED,
        ))
        return TestSuiteResponse(**parsed_resp)

    def get_test_suite(
            self, 
            test_suite_id: str,
            page: Optional[int] = 1,
            page_size: Optional[int] = None) -> PaginatedGetTestSuiteResponse:
        """
        Get reference data for an existing test suite

        :param test_suite_id:
        """
        params = {}
        if page is not None:
            params["page"] = page # type: ignore
        if page_size is not None:
            params["page_size"] = page_size # type: ignore

        parsed_resp = cast(Dict, self.http_client.get(
            f"/bench/test_suites/{test_suite_id}",
            params=params,
            validation_response_code=HTTPStatus.OK,
        ))
        return PaginatedGetTestSuiteResponse(**parsed_resp)

    def get_summary_statistics(
        self,
        test_suite_id: str,
        run_id: Optional[str] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = None,
    ) -> TestSuiteSummaryResponse:
        """
        Get paginated summary statistics of a test suite

        Defaults to page size of 5.

        :param test_suite_id:
        :param run_id:
        :param page:
        :param page_size:
        """

        params = {}
        if run_id is not None:
            params["run_id"] = run_id
        if page is not None:
            params["page"] = page # type: ignore
        if page_size is not None:
            params["page_size"] = page_size # type: ignore
        
        parsed_resp = cast(Dict, self.http_client.get(
            f"/bench/test_suites/{test_suite_id}/runs/summary",
            params=params,
            validation_response_code=HTTPStatus.OK,
        ))
        return TestSuiteSummaryResponse(**parsed_resp)

    def get_runs_for_test_suite(
        self, 
        test_suite_id: str, 
        sort: Optional[str] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = None,
    ) -> PaginatedGetRunsForTestSuiteResponse:
        """
        Get runs for a particular test suite (identified by test_suite_id)

        :param test_suite_id:
        :param sort:
        """

        params = {}
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page # type: ignore
        if page_size is not None:
            params["page_size"] = page_size # type: ignore

        parsed_resp = cast(Dict, self.http_client.get(
            f"/bench/test_suites/{test_suite_id}/runs",
            params=params,
            validation_response_code=HTTPStatus.OK,
        ))
        return PaginatedGetRunsForTestSuiteResponse(**parsed_resp)

    def create_new_test_run(
        self, test_suite_id: str, json_body: CreateRunRequest
    ) -> CreateRunResponse:
        """
        Creates a new test run with model version / associated metadata


        :param test_suite_id:
        :param json_body:
        """

        parsed_resp = cast(Dict, self.http_client.post(
            f"/bench/test_suites/{test_suite_id}/runs",
            json=json_body.json(),
            validation_response_code=HTTPStatus.CREATED,
        ))
        return CreateRunResponse(**parsed_resp)

    def get_test_run(
        self,
        test_suite_id: str,
        test_run_id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = None,
        sort: Optional[bool] = None,
    ) -> PaginatedGetRunResponse:
        """
        Get a test run with input, output, and reference data

        :param test_suite_id:
        :param test_run_id:
        :param page:
        :param page_size:
        :param sort:
        """

        params = {}
        if page is not None:
            params["page"] = page # type: ignore
        if page_size is not None:
            params["page_size"] = page_size # type: ignore
        if sort is not None:
            params["sort"] = sort

        parsed_resp = cast(Dict, self.http_client.get(
            f"/bench/test_suites/{test_suite_id}/runs/{test_run_id}",
            params=params,
            validation_response_code=HTTPStatus.OK,
        ))
        return PaginatedGetRunResponse(**parsed_resp)
    
    def delete_test_suite(self, test_suite_id: str):
        """
        Deletes test suite

        Is idempotent.

        :param test_suite_id:
        """

        raw_resp = self.http_client.delete(
            f"/bench/test_suites/{test_suite_id}",
            validation_response_code=HTTPStatus.NO_CONTENT,
            return_raw_response=True,
        )
        return raw_resp
    
    def delete_test_run(self, test_suite_id: str, test_run_id: str):
        """
        Deletes a test run

        Is idempotent.

        :param test_suite_id:
        :param test_run_id:
        """

        raw_resp = self.http_client.delete(
            f"/bench/test_suites/{test_suite_id}/runs/{test_run_id}",
            validation_response_code=HTTPStatus.NO_CONTENT,
            return_raw_response=True,
        )
        return raw_resp

