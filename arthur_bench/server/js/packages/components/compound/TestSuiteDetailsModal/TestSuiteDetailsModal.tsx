import React from 'react';
import Modal from '@core/Modal/Modal';
import Icon, { EIconType } from '@core/Icon';
import styles from './styles';
import { useFela } from 'react-fela';
import { useTranslation } from 'react-i18next';
import { DetailedTestSuite } from 'arthur-redux/slices/testSuites/types';
import { parseAndFormatDate } from '../InsightHeadline/InsightHeadline';
import MethodTag from "../TestSuiteCard/MethodTag";

type props = {
    testSuite: DetailedTestSuite;
    showModal: boolean;
    setShowModal: (arg: boolean) => void;
};
const TestSuiteDetailsModal = ({
    testSuite,
    showModal,
    setShowModal,
}: props) => {
    const { t } = useTranslation(['common']);
    const { css } = useFela();
    const modelDetail = (
        <div className={css(styles.container)}>
            <div className={css(styles.header)}>
                <div className={css(styles.title)}>{testSuite.name}</div>
                <Icon
                    icon={EIconType.CLOSE_CIRCLE}
                    style={{ cursor: 'pointer' }}
                    color={'black'}
                    size={20}
                    clickHandler={() => setShowModal(!showModal)}
                />
            </div>
            <div className={css(styles.body)}>
                <div className={css(styles.column)}>
                    <div className={css(styles.columnHeader)}>
                        {t('testSuite.generalInformation')}
                    </div>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>
                            {t('testSuite.testSuiteId')}
                        </div>
                        <div>{testSuite.id}</div>
                    </div>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>
                            {t('testSuite.description')}
                        </div>
                        <div>{testSuite.description}</div>
                    </div>
                </div>
                <div className={css(styles.column)}>
                    <div className={css(styles.columnHeader)}>
                        {t('testSuite.testRunInformation')}
                    </div>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>
                            {t('testSuite.scoringMethod')}
                        </div>
                        <MethodTag name={testSuite.scoring_method}/>
                    </div>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>
                            {t('testSuite.lastRun')}
                        </div>
                        <div>{testSuite.last_run_time ? parseAndFormatDate(testSuite.last_run_time) : 'N/A'}</div>
                    </div>
                    <div className={css(styles.dataChunk)}>
                        <div className={css(styles.dataChunkLabel)}>
                            {t('testSuite.number')}
                        </div>
                        <div>{testSuite.num_runs}</div>
                    </div>
                </div>
            </div>
        </div>
    );

    return <Modal children={[modelDetail]} showModal={showModal} setShowModal={setShowModal}/>;
};

export default TestSuiteDetailsModal;
