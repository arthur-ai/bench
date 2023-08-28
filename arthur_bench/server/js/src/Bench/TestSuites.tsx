import React, { useCallback, useEffect, useState } from 'react';
import TestSuiteCard from '@compound/TestSuiteCard/TestSuiteCard';
import { useFela } from 'react-fela';
import styles from './styles';
import TestSuitesHeader from '@compound/TestSuitesHeader/TestSuitesHeader';
import { Paginator } from '@core/Paginator';
import { useTestSuites } from './useTestSuites';
import { useSelector } from 'react-redux';
import { State } from 'arthur-redux/config/state.type';
import HeaderImage from 'resources/images/Arthur_Logo_Symbol_low_margin.svg';
import { TTestSuite } from 'arthur-redux/slices/testSuites/types';
import { useTranslation } from 'react-i18next';
import { Button } from '@core/Button';
import { EIconType } from '@core/Icon';
import { TSelectItem } from '@core/StyledSelect/StyledSelect';
import WelcomeModal from '@compound/WelcomeModal/WelcomeModal';

const PYTHON_LINK = 'https://github.com/arthur-ai/bench';

const EmptyState = () => {
    const { t } = useTranslation(['common']);

    const { css } = useFela();
    return (
        <div className={css(styles.emptyState)}>
            <h3>{t('testSuite.noSuites')}</h3>
            <span>{t('testSuite.getStarted')}</span>
            <Button
                text={t('testSuite.download')}
                iconStart={EIconType.EXTERNAL_LINK}
                clickHandler={() => window.open(PYTHON_LINK)}
            />
        </div>
    );
};
const TestSuites = () => {
    const { css } = useFela();
    const [expandedIndex, setExpandedIndex] = useState<number>(-1);
    const [tablePage, setTablePage] = useState<number>(1);
    const [sortColumn, setSortColumn] = useState<string>('-last_run_time');
    const [filters, setFilters] = useState<TSelectItem[]>([]);
    const { fetchTestSuites } = useTestSuites();

    const { testSuites, pagination } = useSelector(
        (state: State) => ({
            testSuites: state.testSuites?.data,
            pagination: state.testSuites?.pagination,
        })
    );

    useEffect(() => {
        fetchTestSuites(tablePage, 10, filters, sortColumn);
    }, [filters, sortColumn, tablePage]);

    const setNewPage = useCallback(
        (propsPage: number) => {
            const newPage = propsPage + 1;
            if (newPage === tablePage || !newPage || !tablePage) {
                return;
            }
            setTablePage(newPage);
        },
        [tablePage]
    );



    return (
        <div>
            <div className={css(styles.banner)}>
                <img src={HeaderImage} alt={'logo'} />
                <h2>Welcome to LLM Bench!</h2>
            </div>
            <TestSuitesHeader
                setFilters={setFilters}
                filters={filters}
                setSortColumn={setSortColumn}
            />
            <div className={css(styles.container)}>
                {testSuites?.length ? (
                    <>
                        {testSuites.map((suite: TTestSuite, index: number) => (
                            <TestSuiteCard
                                key={suite.id}
                                suite={suite}
                                expandedIndex={expandedIndex}
                                setExpandedIndex={setExpandedIndex}
                                index={index}
                                isExpanded={expandedIndex === index}
                            />
                        ))}
                        <Paginator
                            total={pagination.total_count}
                            page={tablePage - 1}
                            onPageChange={setNewPage}
                            rowsPerPage={pagination.page_size}
                        />
                    </>
                ) : filters.length ? (
                    <div>No results found</div>
                ) : (
                    <>
                        <EmptyState />
                        <Paginator
                            total={pagination.total_count}
                            page={tablePage - 1}
                            onPageChange={setNewPage}
                            rowsPerPage={pagination.page_size}
                        />
                        <WelcomeModal />
                    </>
                )}
            </div>
        </div>
    );
};

export default TestSuites;
