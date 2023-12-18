import React, {useCallback, useEffect, useState} from 'react';
import { Table, TableHeader, TableRow, TableCell } from '../../core/Table';
import { useParams } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { useTestSuites } from '../../../../src/Bench/useTestSuites';
import { State } from 'arthur-redux';
import { TestSuiteCase } from 'arthur-redux/slices/testSuites/types';
import Loading from '../Loading';
import styles, { cellStyles, headerCell } from '../TestRunTable/styles';
import { useFela } from 'react-fela';
import { Paginator } from '../../core/Paginator';
import ExpandableTableCell from '../../core/Table/components/ExpandableTableCell';
import primary from 'resources/colors/Arthur/primary';

type RowProps = {
    testCase: TestSuiteCase;
};

const cellStyle = {
    width: '450px',
    textAlign: 'left' as 'left',
    border: `1px solid ${primary.ashGrey}`,
    padding: '25px',
};
const Row = ({ testCase }: RowProps) => {
    const { css } = useFela();
    return (
        <TableRow>
            <ExpandableTableCell
                content={testCase.input}
                limit={300}
                tableCellProps={{ style: cellStyle }}
            />
            <ExpandableTableCell
                content={testCase.reference_output}
                limit={200}
                tableCellProps={{ style: cellStyle }}
            />
        </TableRow>
    );
};
const InputsOutputsTable = () => {
    const { testSuiteId } = useParams();
    const { fetchTestSuiteData } = useTestSuites();
    const { css } = useFela();
    const [page, setPage] = useState<number>(1);

    useEffect(() => {
        testSuiteId && fetchTestSuiteData(testSuiteId, page, 10);
    }, [testSuiteId, page]);


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

    const { data, pagination } = useSelector((state: State) => ({
        data: state.testSuites?.currentTestSuite?.data?.data,
        pagination: state.testSuites?.currentTestSuite?.data?.pagination,
    }));

    return (
        <>
            <Table className={css(styles.table)}>
                <TableHeader>
                    <TableRow>
                        <TableCell className={css(headerCell())}>
                            <h5>INPUT PROMPTS</h5>
                        </TableCell>
                        <TableCell className={css(headerCell())}>
                            <h5>REFERENCE OUTPUT</h5>
                        </TableCell>
                    </TableRow>
                </TableHeader>
                {data ? (
                    data.test_cases.map((testCase) => (
                        <Row testCase={testCase} />
                    ))
                ) : (
                    <Loading />
                )}
            </Table>
            {pagination && (
                <Paginator
                    page={page - 1}
                    onPageChange={setNewPage}
                    total={pagination.total_count}
                    rowsPerPage={pagination.page_size}
                />
            )}
        </>
    );
};

export default InputsOutputsTable;
