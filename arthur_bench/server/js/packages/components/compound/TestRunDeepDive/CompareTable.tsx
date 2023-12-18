import React, { useCallback, useEffect, useState } from "react";
import { Table, TableHeader, TableRow } from "../../core/Table";
import TableCell from "../../core/Table/components/TableCell";
import ExpandableTableCell from "../../core/Table/components/ExpandableTableCell";
import { Button, EButtonSize, EButtonVariation } from "../../core/Button";
import { EIconType } from "../../core/Icon";
import styles from "./styles";
import { useParams } from "react-router-dom";
import { useFela } from "react-fela";
import primary from "resources/colors/Arthur/primary";
import { chartColorsArray } from "resources/colors/Arthur/graphs";
import { useTranslation } from "react-i18next";
import CompareModal from "./CompareModal";
import { useSelector } from "react-redux";
import { State } from "arthur-redux";
import { Paginator } from "../../core/Paginator";
import { useTestSuites } from "../../../../../js/src/Bench/useTestSuites";
import {ComparedTestRuns, Output, TTestRunData} from "arthur-redux/slices/testSuites/types";
import formatTestRunData from "../../../utils/format-test-runs/format-test-runs"
import scrollToBottom from "../../../utils/scroll-to-bottom/scroll-to-bottom"

type RowProps = {
    testCase: ComparedTestRuns;
};
const Row = ({ testCase }: RowProps) => {
    const { css } = useFela();
    const [showModal, setShowModal] = useState(false);

    return (
        <TableRow>
            <ExpandableTableCell content={<div>{testCase.input}</div>} limit={true} tableCellProps={{ style: styles.expandableTableCell }} />
            {testCase.referenceOutput && (
                <ExpandableTableCell content={testCase.referenceOutput} limit={300} tableCellProps={{ style: styles.expandableTableCell }} />
            )}
            {testCase.outputs.map((output: Output, index: number) => (
                <TableCell style={styles.expandableTableCell}>
                    <ExpandableTableCell content={output.output} limit={300} tableCellProps={{ style: { boxShadow: "none", textAlign: "left" } }} />
                    <p className={css(styles.score(chartColorsArray[index]))}>{output.score}</p>
                </TableCell>
            ))}
            <TableCell>
                <Button
                    size={EButtonSize.SMALL}
                    variation={EButtonVariation.SUBTLE}
                    iconStart={EIconType.EXPAND}
                    clickHandler={() => setShowModal(true)}
                    isLink
                />
            </TableCell>
            <CompareModal testCase={testCase} showModal={showModal} setShowModal={setShowModal} />
        </TableRow>
    );
};
const CompareTable = () => {
    const { css } = useFela();
    const { testSuiteId, testRunIds } = useParams();
    const testRunIdsArray = testRunIds?.split("&").map((param) => param.split("=")[1]);
    const { t } = useTranslation(["common"]);
    const [page, setPage] = useState<number>(1);
    const { fetchMultipleTestRunDetails } = useTestSuites();
    const { pagination, runs } = useSelector((state: State) => ({
        pagination: state.testSuites.currentTestRun?.pagination,
        runs: state.testSuites.currentTestRun?.data,
    }));
    const data = formatTestRunData(runs);
    const columns = runs?.map((run: TTestRunData) => run.name);

    useEffect(() => {
        testSuiteId && testRunIdsArray && fetchMultipleTestRunDetails(testSuiteId, testRunIdsArray, page, 5);
    }, [page]);

    const setNewPage = useCallback(
        (propsPage: number) => {
            const newPage = propsPage + 1;

            if (newPage === page || !newPage || !page) {
                return;
            }
            setPage(newPage);
            scrollToBottom();
        },
        [page]
    );

    return (
        <div className={css(styles.tableBody)}>
            <Table className={css(styles.table)}>
                <TableHeader>
                    <TableCell className={css(styles.headerCell(primary.white))}>{t("testSuite.inputPrompts")}</TableCell>
                    <TableCell className={css(styles.headerCell(primary.white))}>{t("testSuite.referenceOutputs")}</TableCell>
                    {columns.map((column: string) => (
                        <TableCell className={css(styles.headerCell(primary.white))}>{column}</TableCell>
                    ))}
                    <TableCell className={css(styles.headerCell(primary.white))}>{t("testSuite.fullView")}</TableCell>
                </TableHeader>
                {data.map((testCase: ComparedTestRuns) => (
                    <Row testCase={testCase} />
                ))}
            </Table>
            {pagination && (
                <Paginator
                    onPageChange={setNewPage}
                    total={pagination.total_count}
                    page={page - 1}
                    rowsPerPage={pagination.page_size}
                    style={{ marginTop: "20px", color: primary.black }}
                />
            )}
        </div>
    );
};

export default CompareTable;
