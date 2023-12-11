import React, { useEffect } from "react";
import SummaryVisualizations from "@compound/SummaryVisualizations/SummaryVisualizations";
import CompareTable from "@compound/TestRunDeepDive/CompareTable";
import TestSuiteHeader from "../Bench/TestSuiteHeader";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import { useTestSuites } from "../Bench/useTestSuites";
import { State } from "arthur-redux";
import { DetailedTestSuite } from "arthur-redux/slices/testSuites/types";
import { useFela } from "react-fela";
import styles from "./styles";

const CompareTestRuns = () => {
    const { testSuiteId, testRunIds } = useParams();
    const testRunIdsArray = testRunIds?.split("&").map((param) => param.split("=")[1]);

    const { css } = useFela();
    const { fetchTestSuiteData, fetchTestRunSummary } = useTestSuites();

    useEffect(() => {
        if (testSuiteId) {
            fetchTestSuiteData(testSuiteId);
            fetchTestRunSummary(testSuiteId, testRunIdsArray);
        }
    }, []);

    const data = useSelector((state: State) => state.testSuites?.currentTestSuite?.data?.data) as DetailedTestSuite;

    return (
        <div>
            {data && <TestSuiteHeader data={data} isCompare />}
            <div className={css(styles.compareContainer)}>
                <SummaryVisualizations />
                <CompareTable />
            </div>
        </div>
    );
};

export default CompareTestRuns;
