import React from "react";
import styles from "./styles";
import { parseAndFormatDate } from "../InsightHeadline/InsightHeadline";
import { useFela } from "react-fela";
import { useTranslation } from "react-i18next";
import { DetailedTestSuite } from "arthur-redux/slices/testSuites/types";

type Props = {
    testSuite: DetailedTestSuite;
};
const GeneralInformationTab = ({ testSuite }: Props) => {
    const { t } = useTranslation(["common"]);
    const { css } = useFela();

    return (
        <>
            <div className={css(styles.column)}>
                <div className={css(styles.columnHeader)}>{t("testSuite.generalInformation")}</div>
                <div className={css(styles.columnBody)}>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>{t("testSuite.testSuiteId")}</div>
                        <div>{testSuite.id}</div>
                    </div>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>{t("testSuite.description")}</div>
                        <div>{testSuite.description}</div>
                    </div>
                </div>
            </div>
            <div className={css(styles.column)}>
                <div className={css(styles.columnHeader)}>{t("testSuite.testRunInformation")}</div>
                <div className={css(styles.columnBody)}>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>{t("testSuite.lastRun")}</div>
                        <div>{testSuite.last_run_time ? parseAndFormatDate(testSuite.last_run_time) : "N/A"}</div>
                    </div>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>{t("testSuite.number")}</div>
                        <div>{testSuite.num_runs}</div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default GeneralInformationTab;
