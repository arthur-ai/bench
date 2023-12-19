import React from "react";
import { TableCell, TableHeader, TableRow } from "../../core/Table";
import styles from "./styles";
import { useFela } from "react-fela";
import primary from "resources/colors/Arthur/primary";
import secondary from "resources/colors/Arthur/secondary";
import { useTranslation } from "react-i18next";
import { TestRunCase } from "../../../arthur-redux/slices/testSuites/types";

type Props = {
    runs: TestRunCase[];
    isComposite: boolean;
};
const Header = ({ runs, isComposite }: Props) => {
    const { css } = useFela();
    const { t } = useTranslation(["common"]);
    const scorers = (runs.length && runs[0].details) ?? {};
    const { hasScores, hasLabels, hasReference } = (runs || []).reduce(
        (acc, run) => {
            if (run.score_result?.score !== undefined) {
                acc.hasScores = true;
            }

            if (run.label) {
                acc.hasLabels = true;
            }

            if (run.reference_output) {
                acc.hasReference = true;
            }

            return acc;
        },
        { hasScores: false, hasLabels: false, hasReference: false }
    );

    return (
        <TableHeader>
            <TableRow>
                <TableCell className={css(styles.headerCell(secondary.variant.grey.active))}>
                    <h5>{t("testSuite.inputPrompts")}</h5>
                </TableCell>
                {hasReference && (
                    <TableCell className={css(styles.headerCell(secondary.variant.grey.active))}>
                        <h5>{t("testSuite.referenceOutputs")}</h5>
                    </TableCell>
                )}
                <TableCell className={css(styles.headerCell(primary.mint))}>
                    <h5>{t("testSuite.modelOutputs")}</h5>
                </TableCell>
                {hasScores && (
                    <TableCell className={css(styles.headerCell(primary.mint))}>
                        <h5>{isComposite ? t("testSuite.overallScore") : t("testSuite.score")}</h5>
                    </TableCell>
                )}
                {hasLabels && (
                    <TableCell className={css(styles.headerCell(primary.mint))}>
                        <h5>{isComposite ? t("testSuite.overallLabel") : t("testSuite.label")}</h5>
                    </TableCell>
                )}
                {isComposite &&
                    Object.entries(scorers).map(([key, value]) => (
                        <>
                            {value.score !== undefined && (
                                <TableCell key={key} className={css(styles.headerCell(primary.mint))}>
                                    <h5>
                                        {key.toUpperCase()} {t("testSuite.score")}
                                    </h5>
                                </TableCell>
                            )}
                            {value.label && (
                                <TableCell key={key} className={css(styles.headerCell(primary.mint))}>
                                    <h5>
                                        {key.toUpperCase()} {t("testSuite.label")}
                                    </h5>
                                </TableCell>
                            )}
                        </>
                    ))}
            </TableRow>
        </TableHeader>
    );
};

export default Header;
