import React from 'react';
import { useFela } from 'react-fela';
import styles from './styles';
import { Button } from '../../core/Button';
import TestRunTable from '../TestRunTable/TestRunTable';
import { EIconType } from '../../core/Icon';
import { useNavigate } from 'react-router-dom';
import { TTestSuite } from 'arthur-redux/slices/testSuites/types';
import { useTestSuites } from '../../../../src/Bench/useTestSuites';
import { parseAndFormatDate } from '../InsightHeadline/InsightHeadline';
import MethodTag from './MethodTag';

type cardProps = {
    suite: TTestSuite;
    expandedIndex: number;
    setExpandedIndex: (arg: number) => void;
    index: number;
    isExpanded: boolean;
};

const TestSuiteCard = ({
    suite,
    expandedIndex,
    setExpandedIndex,
    isExpanded,
    index,
}: cardProps) => {
    const { css } = useFela();
    const navigate = useNavigate();
    const { fetchTestRuns } = useTestSuites();
    const toggleExpandedIndex = (index: number) => {
        if (index === expandedIndex) {
            setExpandedIndex(-1);
        } else {
            setExpandedIndex(index);
        }
    };
    const handleSelectSuite = (id: string) => {
        navigate(`/bench/${id}/runs`);
        fetchTestRuns(id, 1, 5);
    };

    return (
        <div className={css(styles.container)}>
            <div className={css(styles.row)}>
                <span
                    className={css(styles.name)}
                    onClick={() => handleSelectSuite(suite.id)}
                >
                    {suite.name}
                </span>
                <MethodTag name={suite.scoring_method.name} />
                <span className={css(styles.date)}>
                    Latest Run:{' '}
                    {suite.last_run_time
                        ? parseAndFormatDate(suite.last_run_time)
                        : 'N/A'}
                </span>
            </div>
            <hr className={css(styles.hr)} />
            <div>
                <Button
                    text={isExpanded ? 'CLOSE TEST RUNS' : 'VIEW TEST RUNS'}
                    isLink={true}
                    clickHandler={() => toggleExpandedIndex(index)}
                    iconStart={
                        isExpanded
                            ? EIconType.CHEVRON_UP
                            : EIconType.CHEVRON_RIGHT
                    }
                />
                {isExpanded && <TestRunTable testSuiteId={suite.id} />}
            </div>
        </div>
    );
};

export default TestSuiteCard;
