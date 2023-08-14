import React from 'react';
import AverageScores from './AverageScores';
import RunDistributions from './RunDistributions';
import { useFela } from 'react-fela';
import styles from './styles';
import { useSelector } from 'react-redux';
import { State } from 'arthur-redux';

const EmptyState = () => {
    const { css } = useFela();
    return (
        <div className={css(styles.empty)}>
            <div>No test run data available</div>
        </div>
    )
}
const SummaryVisualizations = () => {
    const { css } = useFela();
    const { summaries, scoring_method, num_test_cases } = useSelector((state: State) => ({
        summaries: state.testSuites.currentTestSuite.summaries.summaries,
        num_test_cases: state.testSuites.currentTestSuite.summaries?.num_test_cases,
        scoring_method: state.testSuites.currentTestSuite.data?.data?.scoring_method.name,

    }));
    return (
        <div>
            <div className={css(styles.container)}>

                    <>
                        <div className={css(styles.chartContainer)}>
                            <div className={css(styles.title)}>
                                Distributions of Top 5 Test Runs
                            </div>
                            <div className={css(styles.subtitle)}>
                                Distribution of scores for the top 5 runs with the highest
                                average score
                            </div>
                            {summaries ? <RunDistributions summaries={summaries} total={num_test_cases}/> : <EmptyState/>}
                        </div>
                        <div className={css(styles.chartContainer)}>
                            {scoring_method && (
                                <>
                                    <div className={css(styles.title)}>{`Top 5 Test Runs by Average ${scoring_method}`}</div>
                                    <div className={css(styles.subtitle)}>{`The average ${scoring_method} scores for the top 5 runs in this suite`}</div>
                                </>
                            )}
                        {summaries ?
                            <AverageScores key={summaries.length} summaries={summaries}/> : <EmptyState/>}
                        </div>
                    </>

            </div>
        </div>
    );
};

export default SummaryVisualizations;
