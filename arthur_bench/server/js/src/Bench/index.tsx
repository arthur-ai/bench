import React, {useEffect} from 'react';
import TestSuiteHeader from '@src/Bench/TestSuiteHeader';
import {Outlet, useParams} from 'react-router-dom';
import {useSelector} from "react-redux";
import { useTestSuites } from './useTestSuites';
import { State } from 'arthur-redux';

const TestSuiteRoute = () => {

    const { testSuiteId } = useParams();
    const { fetchTestSuiteData } = useTestSuites();

    useEffect(() => {
        testSuiteId && (
            fetchTestSuiteData(testSuiteId, 1, 10)
        );
    }, [testSuiteId]);

    const data = useSelector((state: State) => state.testSuites?.currentTestSuite?.data?.data);


    return (
        <>
            {data && <TestSuiteHeader data={data}/>}
            <Outlet />
        </>
    );
};

export default TestSuiteRoute;
