import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useFela } from 'react-fela';
import { useTranslation } from 'react-i18next';
import secondary from 'resources/colors/Arthur/secondary';

import { parseInt as parseIntCustom } from 'utils/parse-int';

import { Button } from '../Button';
import Dropdown from '../Dropdown';
import { EIconType } from '../Icon';
import { EButtonVariation } from '../Button/typings';
import { PaginatorProps, PaginatorState } from './typings';
import {
    defaultStyle,
    textAlign,
    pageButtonStyle,
    dropdownToggleStyle,
    dropdownStyle,
    dropdownButtonStyle,
    pageInputWrap,
    pageInput,
    currentPageStyles,
    rowsPerPageStyles,
    morePage,
    pages,
} from './styles';
import range from 'utils/range';

const DEFAULT_PER_PAGE_OPTIONS = [10, 15, 25];
const DEFAULT_PER_PAGE = 10;
const START_PAGE = 0;

function Paginator(props: PaginatorProps) {
    const [pageNumber, setPageNumber] = useState('');
    const { t } = useTranslation(['common']);
    const { css } = useFela();
    const buttonRef = useRef<HTMLButtonElement>(null);
    const [state, setState] = useState<PaginatorState>({
        openDrop: false,
        page: 0,
        perPage: props.rowsPerPage || 0,
        perPageOpts: [],
    });

    const toggleDrop = () => {
        setState({ ...state, openDrop: !state.openDrop });
    };

    const setPerPage = (value: number) => {
        setState({
            ...state,
            page: START_PAGE,
            perPage: value,
            openDrop: false,
        });
    };

    const changePage = (forward: boolean) => {
        if (forward) {
            setState({ ...state, page: state.page + 1 });
        } else {
            setState({ ...state, page: state.page - 1 });
        }
    };

    const setPage = (page: number) => {
        setState({ ...state, page });
    };

    const { rowsPerPageOptions, rowsPerPage, page: pageProp } = props;

    useEffect(() => {
        let perPageOpts = DEFAULT_PER_PAGE_OPTIONS;
        let perPage = DEFAULT_PER_PAGE;
        let page = START_PAGE;

        if (rowsPerPageOptions?.length) {
            perPageOpts = rowsPerPageOptions.map((opt: number | string) =>
                parseIntCustom(opt),
            );
        }

        if (rowsPerPage) {
            perPage = parseIntCustom(rowsPerPage) as number;
        } else {
            perPage = perPageOpts[0];
        }

        if (typeof pageProp === 'number') {
            page = parseIntCustom(pageProp) as number;
        }

        setState({ perPageOpts, perPage, page, openDrop: false });
    }, [rowsPerPageOptions, rowsPerPage, pageProp]);

    const { page, perPage, perPageOpts, openDrop } = state;
    const { onPageChange, onRowsPerPageChange, allowPageInput } = props;

    useEffect(() => {
        onPageChange(page);
    }, [onPageChange, page]);

    useEffect(() => {
        if (onRowsPerPageChange) {
            onRowsPerPageChange(perPage);
        }
    }, [onRowsPerPageChange, perPage]);

    const totalPages = Math.floor(props.total / (state.perPage || 1)) + 1;

    const handleInputPageNumber = (e: React.KeyboardEvent<HTMLInputElement>) => {
        const newPage = +pageNumber;
        if (e.key === 'Enter') {
            if (!Number.isNaN(newPage) && newPage - 1 < totalPages && newPage) {
                setState({ page: newPage - 1, perPageOpts, perPage, openDrop });
            }
            setPageNumber('');
        }
    };

    const validateNumber = (e: React.KeyboardEvent<HTMLInputElement>) => {
        const numericRegex = /[0-9]|Backspace|Delete|Enter/;
        if (!numericRegex.test(e.key)) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
    };

    const renderPageInput = () => {
        if (!allowPageInput || totalPages <= 1) {
            return null;
        }

        return (
            <div className={css(pageInputWrap)}>
                {t('pagination.goToPage')}
                <input
                    className={css(pageInput)}
                    placeholder="##"
                    value={pageNumber}
                    onChange={(e) => setPageNumber(e.target.value)}
                    onKeyDown={validateNumber}
                    onKeyUp={handleInputPageNumber}
                />
            </div>
        );
    };

    const renderBackButton = () => (
        <Button
            clickHandler={() => {
                changePage(false);
            }}
            variation={EButtonVariation.SUBTLE}
            style={pageButtonStyle}
            testId="paginatorLeft"
            ariaRole="button"
            iconStart={EIconType.CHEVRON_LEFT}
            disabled={props.disabled || low <= 1}
        />
    );

    const renderPage = (p: number) => {
        if (p > 0 && p < totalPages - 1) {
            return renderPageButton(p)
        }

        return null;
    }

    const renderPages = () => {
        let min = state.page - 5 < 0 ? 0 : state.page - 5;
        min = totalPages - 11 < min ? totalPages - 11 : min;
        const pages = range(min, min + 10, 1);
        return <>{pages.map(renderPage)}</>
    }

    const renderPageButton = (pageToShow: number) => {
        return (
            <span role="button" tabIndex={0} onMouseUp={() => setPage(pageToShow)} className={css(morePage, pageToShow === page ? currentPageStyles : {})}>
                {pageToShow + 1}
            </span>
        );
    };

    const { total } = props;
    const low = Math.min(perPage * page + 1, total);
    const high = Math.min(low - 1 + perPage, total);

    const renderForwardButton = useCallback(() => (<Button
        clickHandler={() => changePage(true)}
        variation={EButtonVariation.SUBTLE}
        style={pageButtonStyle}
        testId="paginatorRight"
        ariaRole="button"
        iconStart={EIconType.CHEVRON_RIGHT}
        disabled={props.disabled || page + 1 === totalPages}
    />), [page, totalPages]);

    const renderPageRange = () => {
        if (allowPageInput && totalPages > 1) {
            return (
                <div className={css(pages)}>
                    {renderBackButton()}
                    {renderPageButton(0)}
                    {page > 6 && totalPages > 12 && <span className={css(morePage)}>...</span>}
                    {renderPages()}
                    {page < totalPages - 7 && totalPages > 12 && <span className={css(morePage)}>...</span>}
                    {renderPageButton(totalPages - 1)}
                    {renderForwardButton()}
                </div>
            );
        }

        return (
            <>
                <div className={css(textAlign)}>
                    {t('pagination.pageRange', { low, high, total })}
                </div>
                &nbsp;&nbsp;
                <div>
                    {renderBackButton()}
                    {renderForwardButton()}
                </div>
            </>
        );
    };

    const combinedStyle: React.CSSProperties = {
        minWidth: props.complex ? '350px' : '175px',
        ...defaultStyle,
        ...(props.style ? props.style : {}),
    };

    if (Number.isNaN(props.total) || props.total <= 0) {
        return props.zeroTotalMessage ? <p>{props.zeroTotalMessage}</p> : null;
    }

    return (
        <nav
            className={`${props.className || ''} ${css(combinedStyle)}`}
            role="navigation"
            aria-label="Pagination Navigation"
        >
            {props.complex ? (
                <div className={css(rowsPerPageStyles)}>
                    <div className={css(textAlign)}>
                        {t('pagination.rowsPerPage')}
                    </div>
                    &nbsp;&nbsp;
                    <div>
                        <Button
                            clickHandler={toggleDrop}
                            ref={buttonRef}
                            variation={EButtonVariation.SUBTLE}
                            style={dropdownToggleStyle}
                            testId="pageDropdown"
                            text={perPage}
                            iconEnd={EIconType.ARROW_DOWN}
                            disabled={props.disabled}
                            ariaRole="button"
                        />
                        <Dropdown
                            handleClose={() => {
                            }}
                            actionRef={buttonRef}
                            isOpen={openDrop}
                        >
                            <div className={css({ ...dropdownStyle })}>
                                {perPageOpts.map((x) => (
                                    <button
                                        key={`${x}-perPage`}
                                        onClick={() => {
                                            setPerPage(
                                                parseIntCustom(x) as number,
                                            );
                                        }}
                                        className={css({
                                            ...dropdownButtonStyle,
                                            ':hover': {
                                                backgroundColor:
                                                secondary.lightBlue,
                                            },
                                        })}
                                        data-testid={`${x}-perPage`}
                                    >
                                        {x}
                                    </button>
                                ))}
                            </div>
                        </Dropdown>
                    </div>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                </div>
            ) : null}
            {renderPageRange()}
            {renderPageInput()}
        </nav>
    );
}

export default Paginator;
