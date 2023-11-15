import { TestRunCase } from "../../../arthur-redux/slices/testSuites/types";
import React, {useCallback, useEffect, useState} from 'react';
import { Table, TableCell, TableRow } from '../../core/Table';
import Header from './Header';
import styles from './styles';
import { useFela } from 'react-fela';
import ExpandableTableCell from '../../core/Table/components/ExpandableTableCell';
import primary from 'resources/colors/Arthur/primary';
import {Paginator} from "../../core/Paginator";
import {useSelector} from "react-redux";
import { State } from 'arthur-redux';
import {useParams} from "react-router-dom";
import { useTestSuites } from '../../../../src/Bench/useTestSuites';


type RowProps = {
    runCase: TestRunCase;
};

const cellStyle = {
    maxWidth: '450px',
    textAlign: 'left' as 'left',
    border: `1px solid ${primary.ashGrey}`,
    padding: '25px',
    overflow: 'auto' as 'auto',
    fontSize: '16px'
};
const Row = ({ runCase }: RowProps) => {
    const { css } = useFela();

    return (
        <TableRow>
            <ExpandableTableCell
                text={runCase.input}
                limit={300}
                tableCellProps={{ style: cellStyle }}
            />
            {
                runCase.reference_output &&
                <ExpandableTableCell
                text={runCase.reference_output}
                limit={300}
                tableCellProps={{style: cellStyle}}
            />}
            <ExpandableTableCell
                text={runCase.output}
                limit={300}
                tableCellProps={{ style: cellStyle }}
            />
            <TableCell className={css(styles.cell())}>
                <div>{runCase.score.toFixed(3)}</div>
            </TableCell>
        </TableRow>
    );
};

const TestRunDeepDive = () => {
    const { css } = useFela();
    const [page, setPage] = useState<number>(1);
    const { testSuiteId, testRunId } = useParams();
    const { fetchTestRunDetail } = useTestSuites();
    const { pagination, data } = useSelector((state: State) => ({
        pagination: state.testSuites.currentTestRun?.pagination,
        data: state.testSuites.currentTestRun?.data,
    }));
    useEffect(() => {
        testSuiteId && testRunId && fetchTestRunDetail(testSuiteId, testRunId, page, 10);
    }, [page]);

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

    return (
        <>
            <Table className={css(styles.table)}>
                <Header />
                {data && data.test_case_runs.map((runCase: TestRunCase) => (
                    <Row runCase={runCase} />
                ))}
            </Table>
            {pagination &&
                <Paginator
                    onPageChange={setNewPage}
                    total={pagination.total_count}
                    page={page - 1}
                    rowsPerPage={pagination.page_size}
                    style={{ marginTop: '20px', color: primary.black }}
                />}
        </>
    );
};

export default TestRunDeepDive;
