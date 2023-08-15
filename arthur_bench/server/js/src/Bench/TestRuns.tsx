import React, { useEffect } from 'react';
import TestRunTable from '@compound/TestRunTable/TestRunTable';
import { useFela } from 'react-fela';
import styles from './styles';
import SummaryVisualizations from '@compound/SummaryVisualizations/SummaryVisualizations';
import { useParams } from 'react-router-dom';
import Loading from '@compound/Loading';
import { useTestSuites } from 'arthur-api/hooks/api/useTestSuites';

const TestRuns = () => {
    const { css } = useFela();
    const { testSuiteId } = useParams();
    const { fetchTestRunSummary } = useTestSuites();
    const [loading, setLoading] = React.useState(false);

    useEffect(() => {
        if (testSuiteId) {
            setLoading(true);
            fetchTestRunSummary(testSuiteId).finally(() => {
                setLoading(false);
            });
        }
    }, [testSuiteId]);

    return loading ? (
        <Loading />
    ) : (
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
