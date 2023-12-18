import arthurAxios from "arthur-axios";
import { useDispatch } from "react-redux";
import { useCallback } from "react";
import * as actions from "arthur-redux/slices/testSuites/actions";
import { TPagination } from "arthur-redux/slices/testSuites/types";
import { TSelectItem } from '@core/StyledSelect/StyledSelect';

export const useTestSuites = () => {
    const dispatch = useDispatch();

    const fetchTestSuites = useCallback(
        (page: number, pageSize?: number, filters?: TSelectItem[], sort?: string) => {
            let url = `/api/v3/bench/test_suites?page=${page}&page_size=${pageSize}`;

            if (filters) {
                filters.map((filter) => {
                    url += `&scoring_method=${filter.name}`;
                });
            }
            if (sort) {
                url += `&sort=${sort}`;
            }
            arthurAxios.get(url).then((r) => {
                const pagination: TPagination = {
                    page: r.data.page,
                    page_size: r.data.page_size,
                    total_count: r.data.total_count,
                    total_pages: r.data.total_pages,
                };

                dispatch(
                    actions.fetchTestSuitesReceive({
                        pagination,
                        data: [...r.data.test_suites],
                    })
                );
            });
        },
        [dispatch]
    );

    const fetchTestRuns = useCallback(
        (testSuiteId: string, page: number, pageSize?: number, sort?: string) => {
            let url = `/api/v3/bench/test_suites/${testSuiteId}/runs?page=${page}&page_size=${pageSize}`;

            if (sort) {
                url += `&sort=${sort}`;
            }

            arthurAxios.get(url).then((r) => {
                const pagination: TPagination = {
                    page: r.data.page,
                    page_size: r.data.page_size,
                    total_count: r.data.total_count,
                    total_pages: r.data.total_pages,
                };

                dispatch(
                    actions.fetchTestRunsReceive({
                        pagination,
                        runs: r.data.test_runs,
                    })
                );
            });
        },
        [dispatch]
    );

    const fetchTestSuiteData = useCallback(
        (testSuiteId: string, page?: number, pageSize?: number) => {
            arthurAxios.get(`/api/v3/bench/test_suites/${testSuiteId}?page=${page}&page_size=${pageSize}`).then((r) => {
                const pagination: TPagination = {
                    page: r.data.page,
                    page_size: r.data.page_size,
                    total_count: r.data.total_count,
                    total_pages: r.data.total_pages,
                };
                dispatch(
                    actions.fetchTestSuiteDataReceive({
                        pagination,
                        data: r.data,
                    })
                );
            });
        },
        [dispatch]
    );

    const fetchTestRunSummary = useCallback(
        (testSuiteId: string, testRunIds?: string[]): Promise<void> => {
            let url = `/api/v3/bench/test_suites/${testSuiteId}/runs/summary?`;

            if (testRunIds) {
                url += testRunIds.map((testRunId) => `run_ids=${testRunId}`).join("&");
            }

            return arthurAxios.get(url).then((r) => {
                dispatch(
                    actions.fetchTestRunSummaryReceive({
                        summaries: r.data.summary,
                        num_test_cases: r.data.num_test_cases,
                    })
                );
            });
        },
        [dispatch]
    );

    const fetchTestRunDetail = useCallback(
        (testSuiteId: string, testRunId: string, page?: number, pageSize?: number) => {
            arthurAxios.get(`/api/v3/bench/test_suites/${testSuiteId}/runs/${testRunId}?page=${page}&page_size=${pageSize}`).then((r) => {
                const { page, page_size, total_count, total_pages, ...currentTestRun } = r.data;

                const pagination: TPagination = {
                    page,
                    page_size,
                    total_count,
                    total_pages,
                };

                dispatch(
                    actions.fetchTestRunDetailsReceive({
                        pagination,
                        data: [currentTestRun],
                    })
                );
            });
        },
        [dispatch]
    );

    const fetchMultipleTestRunDetails = useCallback(
        (testSuiteId: string, testRunIds: string[], page?: number, pageSize?: number) => {
            const promises = testRunIds.map((testRunId) => {
                return arthurAxios.get(`/api/v3/bench/test_suites/${testSuiteId}/runs/${testRunId}?page=${page}&page_size=${pageSize}`);
            });

            Promise.all(promises).then((responses) => {
                const data = responses.map((response) => {
                    const { page, page_size, total_count, total_pages, ...currentTestRun } = response.data;

                    const pagination: TPagination = {
                        page,
                        page_size,
                        total_count,
                        total_pages,
                    };

                    return {
                        pagination,
                        data: currentTestRun,
                    };
                });

                dispatch(
                    actions.fetchTestRunDetailsReceive({
                        pagination: data[0].pagination,
                        data: data.map((d) => d.data),
                    })
                );
            });
        },
        [dispatch]
    );

    return {
        fetchTestSuites,
        fetchTestRuns,
        fetchTestSuiteData,
        fetchTestRunSummary,
        fetchTestRunDetail,
        fetchMultipleTestRunDetails,
    };
};
