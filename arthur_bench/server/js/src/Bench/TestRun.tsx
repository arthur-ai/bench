import React, { useEffect, useState } from "react";
import Breadcrumbs from "@core/Breadcrumbs";
import { useTestSuites } from "../Bench/useTestSuites";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import { State } from "arthur-redux";
import Loading from "@compound/Loading";
import Icon, { EIconType } from "@core/Icon";
import SummaryVisualizations from "@compound/SummaryVisualizations/SummaryVisualizations";
import styles from "./styles";
import { useFela } from "react-fela";
import TestRunDeepDive from "@compound/TestRunDeepDive/TestRunDeepDive";
import { useTranslation } from "react-i18next";

const TestRun = () => {
    const { fetchTestRunSummary, fetchTestSuiteData, fetchTestRunDetail } = useTestSuites();
    const { testSuiteId, testRunId } = useParams();
    const [isExpanded, setIsExpanded] = useState(true);
    const { css } = useFela();
    const { t } = useTranslation(["common"]);
    const sort = "score"

    const toggleExpanded = () => {
        setIsExpanded((prevState) => !prevState);
    };

    useEffect(() => {
        if (testSuiteId && testRunId) {
            fetchTestRunDetail(testSuiteId, testRunId, 1, 10, sort);
            fetchTestSuiteData(testSuiteId, 1, 5);
            fetchTestRunSummary(testSuiteId);
            fetchTestRunSummary(testSuiteId, [testRunId]);
        }
    }, [testSuiteId]);

    const { currentTestRun, name } = useSelector((state: State) => ({
        currentTestRun: state.testSuites.currentTestRun?.data,
        name: state.testSuites.currentTestSuite.data?.data?.name,
    }));

    const breadcrumbs = [
        {
            link: "/bench",
            label: "Home",
        },
        {
            link: `/bench/${currentTestRun?.[0]?.test_suite_id}/runs`,
            label: name ?? "",
        },
        {
            link: "#3",
            label: currentTestRun?.[0]?.name ?? "",
        },
    ];

    return (
        <>
            {currentTestRun[0] ? (
                <>
                    <div className={css(styles.header)}>
                        <Breadcrumbs items={breadcrumbs} />
                        <h2>{currentTestRun[0].name}</h2>
                    </div>
                    <div className={css(styles.drawer)}>
                        <div>
                            <Icon
                                size={16}
                                icon={isExpanded ? EIconType.CHEVRON_UP : EIconType.CHEVRON_DOWN}
                                style={{ marginRight: "10px" }}
                                clickHandler={toggleExpanded}
                            />
                            <span>{t("bench.summaryVisualizations")}</span>
                        </div>
                        {isExpanded && <SummaryVisualizations />}
                    </div>
                    <div className={css(styles.tableContainer)}>
                        <TestRunDeepDive />
                    </div>
                </>
            ) : (
                <Loading />
            )}
        </>
    );
};

export default TestRun;
