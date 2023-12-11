import React from 'react';
import {useRoutes } from 'react-router-dom';
import TestSuites from '../Bench/TestSuites';
import TestSuiteRoute from '../Bench/index';
import TestRuns from '../Bench/TestRuns';
import InputsOutputs from '../Bench/InputsOutputs';
import TestRun from '../Bench/TestRun';
import CompareTestRuns from "@src/Bench/CompareTestRuns";

const ArthurRoutes = () => {

    const routes = [

        {
            path: '/bench',
            element: <TestSuites />,
        },
        {
            path: '/bench/:testSuiteId',
            element: <TestSuiteRoute/>,
            children: [
                { path: 'runs', element: <TestRuns /> },
                { path: 'inputs-outputs', element: <InputsOutputs /> },
            ],
        },
        {
            path: '/bench/:testSuiteId/runs/:testRunId',
            element: <TestRun />
        },
        {
            path: "/bench/:testSuiteId/compare/:testRunIds",
            element: <CompareTestRuns />
        },
        {
            path: '*',
            element: <TestSuites/>
        },
    ];

    return useRoutes(routes);
};

export default ArthurRoutes;
