import React from "react";
import AverageScores from "./AverageScores";
import RunDistributions from "./RunDistributions";
import { useFela } from "react-fela";
import styles from "./styles";
import { useSelector } from "react-redux";
import { State } from "arthur-redux";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import CategoricalDistribution from "./CategoricalDistribution";

const EmptyState = () => {
    const { css } = useFela();
    const { t } = useTranslation(["common"]);

    return (
        <div className={css(styles.empty)}>
            <div>{t("visualization.noData")}</div>
        </div>
    );
};

const SummaryVisualizations = () => {
    const { css } = useFela();
    const { t } = useTranslation(["common"]);
    const params = useParams();
    const averageScoresKey = `${params.testSuiteId}-${params.testRunId || ""}`;
    const { summaries, scoring_method, num_test_cases, categorical } = useSelector((state: State) => ({
        summaries: state.testSuites.currentTestSuite.summaries.summaries,
        num_test_cases: state.testSuites.currentTestSuite.summaries?.num_test_cases,
        scoring_method: state.testSuites.currentTestSuite.data?.data?.scoring_method.name,
        categorical: state.testSuites.currentTestSuite.summaries?.categorical,
    }));

    return (
        <div>
            <div className={css(styles.container)}>
                {summaries && categorical ? (
                    <CategoricalDistribution summaries={summaries} total={num_test_cases} />
                ) : (
                    <>
                        <div className={css(styles.chartContainer)}>
                            <div className={css(styles.title)}>{t("visualization.distributionTitle")}</div>
                            <div className={css(styles.subtitle)}>{t("visualization.distributionDescription")}</div>
                            {summaries ? <RunDistributions summaries={summaries} total={num_test_cases} /> : <EmptyState />}
                        </div>
                        <div className={css(styles.chartContainer)}>
                            {scoring_method && (
                                <>
                                    <div className={css(styles.title)}>{t("visualization.averageTitle", { scoring_method: scoring_method })}</div>
                                    <div className={css(styles.subtitle)}>
                                        {t("visualization.averageDescription", { scoring_method: scoring_method })}
                                    </div>
                                </>
                            )}
                            {summaries ? <AverageScores key={averageScoresKey} summaries={summaries} /> : <EmptyState />}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default SummaryVisualizations;
