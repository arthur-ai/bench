import {
    ActionReducerMapBuilder,
    createReducer,
    PayloadAction,
} from '@reduxjs/toolkit';
import { TRunData, Summary, TTestRun, TTestSuiteData, TTestSuitesState} from './types';
import * as actions from './actions';

const defaultState = {
    currentTestSuite: {
        runs: {
            runs: null,
            pagination: { total_count: 0, page: 1, page_size: 0, total_pages: 0 }
        },
        summaries: {
            summaries: null,
            num_test_cases: 0,
            categorical: false
        },
        data: {
            data: null,
            pagination: { total_count: 0, page: 1, page_size: 0, total_pages: 0 }},

    },
    currentTestRun: {
        data: null,
        pagination: { total_count: 0, page: 1, page_size: 0, total_pages: 0 }
    },
    data: null,
    pagination: { total_count: 0, page: 1, page_size: 0, total_pages: 0 },
};

export const testSuitesReducer = createReducer<TTestSuitesState>(
    defaultState,
    (builder: ActionReducerMapBuilder<TTestSuitesState>) => {
        builder
            .addCase(
                actions.fetchTestSuitesReceive,
                (state: TTestSuitesState, action: PayloadAction<any>) => {
                    state.data = action.payload.data;
                    state.pagination = action.payload.pagination;
                }
            )
            .addCase(
                actions.fetchTestRunsReceive,
                (state: TTestSuitesState, action: PayloadAction<TRunData>) => {
                    if (state.currentTestSuite && state.currentTestSuite.runs) {
                        state.currentTestSuite.runs.runs = action.payload.runs;
                        state.currentTestSuite.runs.pagination = action.payload.pagination;
                    }
                }
            )
            .addCase(
                actions.fetchTestSuiteDataReceive,
                (state: TTestSuitesState, action: PayloadAction<TTestSuiteData>) => {
                    if (state.currentTestSuite && state.currentTestSuite.data) {
                        state.currentTestSuite.data.data = action.payload.data;
                        state.currentTestSuite.data.pagination = action.payload.pagination;
                    }
                }
            )
            .addCase(
                actions.fetchTestRunSummaryReceive,
                (state: TTestSuitesState, action: PayloadAction<Summary>) => {
                    if (state.currentTestSuite) {
                        state.currentTestSuite.summaries.summaries = action.payload.summaries;
                        state.currentTestSuite.summaries.num_test_cases = action.payload.num_test_cases;
                        state.currentTestSuite.summaries.categorical = action.payload.categorical;
                    }
                }
            )
            .addCase(
                actions.fetchTestRunDetailsReceive,
                (state: TTestSuitesState, action: PayloadAction<TTestRun>) => {
                    state.currentTestRun.data = action.payload.data;
                    state.currentTestRun.pagination = action.payload.pagination;
                }
            );
    }
);
