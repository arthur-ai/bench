import React, { useCallback, useEffect, useState } from "react";
import { Table, TableCell, TableHeader } from "../../core/Table";
import HeaderCell from "./TestRunHeader";
import TestRunRow from "./TestRunRow";
import { useFela } from "react-fela";
import styles from "./styles";
import { Paginator } from "../../core/Paginator";
import { useTestSuites } from "../../../../../js/src/Bench/useTestSuites";
import { useSelector } from "react-redux";
import { State } from "arthur-redux";
import { Run } from "arthur-redux/slices/testSuites/types";
import { useNavigate, useParams } from "react-router-dom";
import { Button, EButtonSize } from "../../core/Button";
import { useTranslation } from "react-i18next";

type TTableProps = {
    testSuiteId?: string;
    testSuiteName?: string;
};

export type TColumn = {
    asc: string;
    desc: string;
    name: string;
};

const columns: TColumn[] = [
    { asc: "updated_at", desc: "-updated_at", name: "TIMESTAMP" },
    { asc: "name", desc: "-name", name: "TEST RUN NAME" },
    { asc: "avg_score", desc: "-avg_score", name: "AVG SCORE" },
];

const EmptyState = () => {
    const { css } = useFela();

    return (
        <div className={css(styles.empty)}>
            <h3>No test runs created yet</h3>
            <div>Upload your first run through the SDK</div>
            <Button text={"read more"} />
        </div>
    );
};

const TestRunTable = (props: TTableProps) => {
    const { t } = useTranslation(["common"]);
    const { testSuiteId: testId } = useParams();
    const testSuiteId = props.testSuiteId ?? testId;
    const { fetchTestRuns } = useTestSuites();
    const navigate = useNavigate();
    const [sort, setSort] = useState<string>("");
    const [selectedSort, setSelectedSort] = useState<TColumn>({
        asc: "",
        desc: "",
        name: "",
    });
    const [page, setPage] = useState<number>(1);
    const [selectedTestRuns, setSelectedTestRuns] = useState<Run[]>([]);
    const { css } = useFela();
    const { runs, pagination } = useSelector((state: State) => ({
        runs: state.testSuites?.currentTestSuite?.runs?.runs,
        pagination: state.testSuites?.currentTestSuite?.runs?.pagination,
    }));

    useEffect(() => {
        testSuiteId && fetchTestRuns(testSuiteId, page, 5, sort);
    }, [testSuiteId, page, sort]);

    const setNewPage = useCallback(
        (propsPage: number) => {
            const newPage = propsPage + 1;

            if (newPage === page || !newPage || !page) {
                return;
            }
            setPage(newPage);
        },
        [page]
    );

    const newUrl: string = `/bench/${testSuiteId}/compare/${selectedTestRuns.map((run) => `test_run_id=${run.id}`).join("&")}`;

    return (
        <>
            {runs && runs.length > 0 && testSuiteId && pagination ? (
                <div className={css(styles.container)}>
                    <div className={css(styles.button)}>
                        <div>{t("testSuite.select")}</div>
                        <Button
                            text={t("testSuite.compare")}
                            size={EButtonSize.SMALL}
                            disabled={selectedTestRuns.length < 2 || selectedTestRuns.length >= 5}
                            clickHandler={() => navigate(newUrl)}
                        />
                    </div>
                    <div className={css(styles.tableContainer)}>
                        <Table className={css(styles.table)}>
                            <TableHeader>
                                <TableCell> </TableCell>
                                {columns.map((column) => (
                                    <HeaderCell
                                        sort={sort}
                                        setSort={setSort}
                                        column={column}
                                        selectedSort={selectedSort}
                                        setSelectedSort={setSelectedSort}
                                        key={column.name}
                                    />
                                ))}
                            </TableHeader>
                            {runs.map((run: Run) => (
                                <TestRunRow
                                    testRun={run}
                                    testSuiteId={testSuiteId}
                                    key={run.id}
                                    selectedTestRuns={selectedTestRuns}
                                    setSelectedTestRuns={setSelectedTestRuns}
                                />
                            ))}
                        </Table>
                        <Paginator
                            onPageChange={setNewPage}
                            rowsPerPage={pagination.page_size}
                            total={pagination.total_count}
                            style={{ fontSize: "14px", marginLeft: "20px" }}
                            page={page - 1}
                        />
                    </div>
                </div>
            ) : (
                <>
                    <EmptyState />
                </>
            )}
        </>
    );
};

export default TestRunTable;
