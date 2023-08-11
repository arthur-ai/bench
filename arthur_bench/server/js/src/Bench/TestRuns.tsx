import React from 'react';
import TestRunTable from '@compound/TestRunTable/TestRunTable';
import { useFela } from 'react-fela';
import styles from './styles';
import SummaryVisualizations from '@compound/SummaryVisualizations/SummaryVisualizations';

const TestRuns = () => {
    const { css } = useFela();
    return (
        <div>
            <div className={css(styles.middleRow)}>
                <div>Summary Visualizations</div>
                <SummaryVisualizations />
            </div>
            <div className={css(styles.bottomRow)}>
                <div>Test Runs</div>
                <TestRunTable />
            </div>
        </div>
    );
};

export default TestRuns;
