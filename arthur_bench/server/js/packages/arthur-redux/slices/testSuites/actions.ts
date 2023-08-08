import {createAction} from "@reduxjs/toolkit";
import * as constants from "../testSuites/constants";



export const fetchTestSuitesRequest = createAction(
    constants.FETCH_TEST_SUITES_REQUEST
);
export const fetchTestSuitesReceive = createAction<any>(
    constants.FETCH_TEST_SUITES_RECEIVE
);
export const fetchTestRunsRequest = createAction(
    constants.FETCH_TEST_RUNS_REQUEST
);
export const fetchTestRunsReceive = createAction<any>(
    constants.FETCH_TEST_RUNS_RECEIVE
);
export const fetchTestSuiteDataRequest = createAction(
    constants.FETCH_TEST_SUITE_DATA_REQUEST
);
export const fetchTestSuiteDataReceive = createAction<any>(
    constants.FETCH_TEST_SUITE_DATA_RECEIVE
);
export const fetchTestRunSummaryRequest = createAction(
    constants.FETCH_TEST_RUN_SUMMARY_REQUEST
);
export const fetchTestRunSummaryReceive = createAction<any>(
    constants.FETCH_TEST_RUN_SUMMARY_RECEIVE
);
export const fetchTestRunDetailsRequest = createAction(
    constants.FETCH_TEST_RUN_DETAILS_REQUEST
);
export const fetchTestRunDetailsReceive = createAction<any>(
    constants.FETCH_TEST_RUN_DETAILS_RECEIVE
);
