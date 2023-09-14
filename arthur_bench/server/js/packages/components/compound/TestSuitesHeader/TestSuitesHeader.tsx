import React from 'react';
import { useFela } from 'react-fela';
import styles from './styles';
import MetricDropdownSelection from '../MetricsDropdownSelection';
import { TSelectItem } from '../../core/StyledSelect/StyledSelect';
import SortDropdown from '../SortDropdown/SortDropdown';

const metrics = [
    { id: '1', name: 'bertscore' },
    { id: '2', name: 'summary_quality' },
    { id: '3', name: 'qa_correctness' },
    { id: '4', name: 'exact_match' },
    { id: '5', name: 'hallucination' },
    { id: '6', name: 'readability' },
    { id: '7', name: 'word_count_match' },
    { id: '8', name: 'specificity' },
    { id: '9', name: 'hedging_language' },
    { id: '10', name: 'python_unit_testing' },
];
const sortOptions = [
    { id: 'last_run_time', name: 'OLDEST FIRST' },
    { id: '-last_run_time', name: 'NEWEST FIRST' },
    { id: 'name', name: 'TEST SUITE NAME: A-Z' },
    { id: '-name', name: 'TEST SUITE NAME: Z-A' }

];
type Props = {
    setFilters: (arg: TSelectItem[]) => void;
    filters: TSelectItem[];
    setSortColumn: (arg: string) => void;
};
const TestSuitesHeader = (props: Props) => {
    const { css } = useFela();
    const { setFilters, filters, setSortColumn } = props;
    return (
        <div className={css(styles.container)}>
            <h2>Test Suites</h2>
            <div className={css(styles.toolbar)}>
                <MetricDropdownSelection
                    data={metrics}
                    onChange={setFilters}
                    selectedItems={filters}
                    label={'SCORING METHODS'}
                />
                <SortDropdown
                    sortOptions={sortOptions}
                    setSortColumn={setSortColumn}
                />
            </div>
        </div>
    );
};

export default TestSuitesHeader;
