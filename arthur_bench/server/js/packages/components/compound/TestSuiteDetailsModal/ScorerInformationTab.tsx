import styles from "./styles";
import MethodTag from "../TestSuiteCard/MethodTag";
import React from "react";
import { useTranslation } from "react-i18next";
import { useFela } from "react-fela";
import { DetailedTestSuite } from "arthur-redux/slices/testSuites/types";

type Props = {
    testSuite: DetailedTestSuite;
};

const ScorerInformationTab = ({ testSuite }: Props) => {
    const { t } = useTranslation(["common"]);
    const { css } = useFela();

    return (
        <>
            <div className={css(styles.column)}>
                <div className={css(styles.columnHeader)}>{t("testSuite.scoringInformation")}</div>
                <div className={css(styles.columnBody)}>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>{t("testSuite.scoringMethod")}</div>
                        <MethodTag name={testSuite.scoring_method.name} />
                    </div>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>{t("testSuite.type")}</div>
                        <div>{testSuite.scoring_method.type}</div>
                    </div>
                    {testSuite.scoring_method.config && (
                        <div className={css(styles.dataChunk)}>
                            <div className={css(styles.dataChunkLabel)}>{t("testSuite.configurations")}</div>
                            <div className={css(styles.dataChunkBody)}>
                                {Object.entries(testSuite.scoring_method.config).map(([key, value]: [string, string]) => {
                                    return (
                                        <div key={key}>
                                            {key}: {value}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    )}
                </div>
            </div>
            <div className={css(styles.column)}>
                <div className={css(styles.columnHeader)}>{t("testSuite.scoringMethodBreakdown")}</div>
                <div className={css(styles.columnBody)}>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>{t("testSuite.calculation")}</div>
                        <div>Coming soon!</div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default ScorerInformationTab;
