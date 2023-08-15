import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Breadcrumbs from '@core/Breadcrumbs';
import Tabs from '@core/Tabs';
import { Button } from '@core/Button';
import { EIconType } from '@core/Icon';
import TestSuiteDetailsModal from '@compound/TestSuiteDetailsModal/TestSuiteDetailsModal';
import styles from './styles';
import { useFela } from 'react-fela';
import { useTestSuites } from './useTestSuites';
import { DetailedTestSuite } from 'arthur-redux/slices/testSuites/types';
import MethodTag from '@compound/TestSuiteCard/MethodTag';
import { useTranslation } from 'react-i18next';

type Props = {
    data: DetailedTestSuite;
};
const TestSuiteHeader = ({ data }: Props) => {
    const navigate = useNavigate();
    const [showModal, setShowModal] = useState(false);
    const { css } = useFela();
    const { t } = useTranslation(['common']);
    const { fetchTestRunSummary } = useTestSuites();

    enum Tab {
        TestRuns = 'runs',
        InputsOutputs = 'inputs-outputs',
    }

    const tabs: { label: string; id: string; route: Tab }[] = [
        {
            label: t('testSuite.testRuns'),
            id: '1',
            route: Tab.TestRuns,
        },
        {
            label: t('testSuite.inputsOutputs'),
            id: '2',
            route: Tab.InputsOutputs,
        },
    ];

    const breadcrumbs = [
        {
            link: '/bench',
            label: t('testSuite.home'),
        },
        {
            link: '#2',
            label: data.name,
        },
    ];

    useEffect(() => {
        fetchTestRunSummary(data.id);
    }, [data]);

    const toggleShowModal = () => {
        setShowModal(!showModal);
    };

    const [selectedTab, setSelectedTab] = useState('1');

    const handleTabClick = (selectedTabId: string) => {
        setSelectedTab(selectedTabId);
        const mappedTab = tabs.find((tab) => tab.id === selectedTabId);
        mappedTab && navigate(`/bench/${data.id}/${mappedTab.route}`);
    };

    useEffect(() => {
        const locationPath = location.pathname.split('/')[3];
        const mappedTab = tabs.find((tab) => tab.route === locationPath);
        mappedTab && setSelectedTab(mappedTab.id);
    }, [location]);

    return (
        <div className={css(styles.header)}>
            <Breadcrumbs items={breadcrumbs} />
            <div className={css(styles.topRow)}>
                <div className={css(styles.topRow)}>
                    <h2>{data.name}</h2>
                    <MethodTag name={data.scoring_method.name} />
                </div>
                <Button
                    iconStart={EIconType.DETAILS}
                    text={t('testSuite.details')}
                    clickHandler={toggleShowModal}
                    isLink={true}
                />
                <TestSuiteDetailsModal
                    testSuite={data}
                    showModal={showModal}
                    setShowModal={setShowModal}
                />
            </div>
            <Tabs
                tabs={tabs}
                selectedTabId={selectedTab}
                onTabClick={handleTabClick}
            />
        </div>
    );
};

export default TestSuiteHeader;
