import { TestRunCase } from "../../../arthur-redux/slices/testSuites/types"
import React, { useCallback, useEffect, useState } from "react";
import { Table, TableCell, TableRow } from "../../core/Table";
import Header from "./Header";
import styles from "./styles";
import { useFela } from "react-fela";
import ExpandableTableCell from "../../core/Table/components/ExpandableTableCell";
import primary from "resources/colors/Arthur/primary";
import { Paginator } from "../../core/Paginator";
import { useSelector } from "react-redux";
import { State } from "arthur-redux";
import { useParams } from "react-router-dom";
import { useTestSuites } from "../../../../../js/src/Bench/useTestSuites";
import scrollToBottom from "../../../utils/scroll-to-bottom/scroll-to-bottom"

type RowProps = {
    runCase: TestRunCase;
    hasScores?: boolean;
    hasLabels?: boolean;
};

export const cellStyle = {
    maxWidth: "450px",
    minWidth: "300px",
    textAlign: "left" as const,
    border: `1px solid ${primary.ashGrey}`,
    padding: "25px",
    overflow: "auto" as const,
    fontSize: "16px",
};
const Row = ({ runCase, hasScores, hasLabels }: RowProps) => {
    const { css } = useFela();

    return (
        <TableRow>
            <ExpandableTableCell content={runCase.input} limit={300} tableCellProps={{ style: cellStyle }} />
            {runCase.reference_output && <ExpandableTableCell content={runCase.reference_output} limit={300} tableCellProps={{ style: cellStyle }} />}
            <ExpandableTableCell content={runCase.output} limit={300} tableCellProps={{ style: cellStyle }} />
            {hasScores && (
                <TableCell className={css(styles.cell())}>
                    <div>{runCase.score_result?.score !== undefined ? runCase.score_result.score.toFixed(3) : "N/A"}</div>
                </TableCell>
            )}
            {hasLabels && (
                <TableCell className={css(styles.cell())}>
                    <div>{runCase.label ?? "N/A"}</div>
                </TableCell>
            )}
            {runCase.details &&
                Object.entries(runCase.details).map(([key, value]) => (
                    <>
                        {value.score !== undefined && (
                            <TableCell key={key} className={css(styles.cell())}>
                                <h5>{value.score.toFixed(3)}</h5>
                            </TableCell>
                        )}
                        {value.label && (
                            <TableCell key={key} className={css(styles.cell())}>
                                <h5>{value.label}</h5>
                            </TableCell>
                        )}
                    </>
                ))}
        </TableRow>
    );
};

const TestRunDeepDive = () => {
    const { css } = useFela();
    const [page, setPage] = useState<number>(0);
    const { testSuiteId, testRunId } = useParams();
    const { fetchTestRunDetail } = useTestSuites();
    const { pagination, runs } = useSelector((state: State) => ({
        pagination: state.testSuites.currentTestRun?.pagination,
        runs: state.testSuites.currentTestRun?.data[0]?.test_case_runs,
    }));
    useEffect(() => {
        testSuiteId && testRunId && fetchTestRunDetail(testSuiteId, testRunId, page, 10);
    }, [page]);

    const { hasScores, hasLabels, isComposite } = (runs || []).reduce(
        (acc, run: TestRunCase) => {
            if (run.score_result?.score !== undefined) {
                acc.hasScores = true;
            }

            if (run.label) {
                acc.hasLabels = true;
            }

            if (run.details) {
                acc.isComposite = true;
            }

            return acc;
        },
        { hasScores: false, hasLabels: false, isComposite: false }
    );

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
        <>
            <Table className={css(styles.table)}>
                {runs && (
                    <>
                        <Header runs={runs} isComposite={isComposite} />
                        {runs.map((runCase: TestRunCase) => (
                            <Row runCase={runCase} hasScores={hasScores} hasLabels={hasLabels} />
                        ))}
                    </>
                )}
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
        </>
    );
};

export default TestRunDeepDive;
