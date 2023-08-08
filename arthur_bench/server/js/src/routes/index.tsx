import React from 'react';
import {useRoutes } from 'react-router-dom';
/* Model component and children */

import TestSuites from '../Bench/TestSuites';
import TestSuiteRoute from '../Bench/index';
import TestRuns from '../Bench/TestRuns';
import InputsOutputs from '../Bench/InputsOutputs';
import TestRun from '../Bench/TestRun';

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
            path: '*',
            element: <TestSuites/>
        },
    ];

    return useRoutes(routes);
};

export default ArthurRoutes;
