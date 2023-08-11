import React, { useEffect, useRef, useState } from 'react';
import { useFela } from 'react-fela';
import { useTranslation } from 'react-i18next';

import FilterComponent from '../FilterComponent';
import Icon, { EIconType } from '@core/Icon';
import Search from '@core/Search';
import Dropdown from '@core/Dropdown';
import Chip, { TChip } from '@compound/Chip';

import {
    defaultStyle,
    optionStyle,
    searchStyles,
    selectedAreaStyle,
    selectedTagColumn,
    optionsStyles,
    selectedTagStyle,
    dropdownRootStyles,
    optionsDropdownFooter,
    optionStyleContainer,
    optionStylesContainer,
    renderSelectAllContainer,
    searchContainer,
    paginationContainer,
} from './styles';
import { IMetricDropdownSelectionProps } from './typings';
import { TSelectItem } from '@core/StyledSelect/StyledSelect';
import styles from '@core/StyledSelect/styles';
import { Paginator } from '../../core/Paginator';
import { EButtonVariation, Button, EButtonSize } from '../../core/Button';
import secondary from 'resources/colors/Arthur/secondary';

function MetricDropdownSelection<T extends TSelectItem>(
    props: IMetricDropdownSelectionProps<T>
) {
    const { data, onChange, selectedItems, label, handleApply } = props;
    const { css } = useFela();
    const { t } = useTranslation(['common']);
    const divRef = useRef<HTMLDivElement>(null);
    const [open, setOpen] = useState(false);
    const [filteredOptions, setFilteredOptions] = useState<T[]>(props.data);
    const [searchValue, setSearchValue] = useState('');

    useEffect(() => setFilteredOptions(data), [data]);

    useEffect(() => {
        if (searchValue) {
            setFilteredOptions(data.filter(handleFilterItems));
        } else {
            setFilteredOptions(data);
        }
    }, [searchValue]);

    const handleUnselectItem = (item: TChip | T) =>
        onChange(selectedItems.filter((i) => i.id !== item.id));

    const handleSelectItem = (item: T) => onChange([...selectedItems, item]);

    const handleBlurSearch = () => setSearchValue('');

    const handleFilterItems = (item: T) =>
        item.name.toLocaleLowerCase().includes(searchValue.toLocaleLowerCase());

    const handleSelectAll = () => {
        if (selectedItems.length === data.length) {
            onChange([]);
        } else {
            onChange(data);
        }
    };

    const handleClearAll = () => {
        onChange([]);
    };

    const handleApplyAll = () => {
        // to do: set applied filters
        setOpen(false);
        handleApply()
    };

    const toggleDrop = () => setOpen(!open);

    const renderLabel = () => {
        if (selectedItems.length) {
            return `Selected ${label} (${selectedItems.length})`;
        } else {
            return `All ${label}`;
        }
    };

    const renderSelectAll = () => (
        <div
            onMouseDown={handleSelectAll}
            tabIndex={0}
            role='button'
            style={renderSelectAllContainer}
        >
            <FilterComponent
                label={t('filter.selectAll')}
                type='selection'
                isActive={data.length === selectedItems.length}
                style={optionStyle}
                color={secondary.blue}
                bkgColor={secondary.lightBlue}
            />
        </div>
    );

    const renderFilteredOptions = () =>
        
        filteredOptions.map((item) => {
            
            const isActive = selectedItems.map(selItem => selItem.id).includes(item.id);
            const itemAction = () =>
                isActive ? handleUnselectItem(item) : handleSelectItem(item);
               
            return (
                <div
                    onMouseDown={itemAction}
                    tabIndex={0}
                    role='button'
                    key={item.id}
                    style={optionStyleContainer}
                >
                    <FilterComponent
                        label={item.name}
                        type='selection'
                        isActive={isActive}
                        style={optionStyle}
                        color={secondary.blue}
                        bkgColor={secondary.lightBlue}
                    />
                </div>
            );
        });

    const renderSelectedTags = () =>
        selectedItems.map((selectedItem: T) => (
            <Chip
                overrideStyles={selectedTagStyle}
                key={selectedItem.id}
                chip={selectedItem}
                iconEnd={EIconType.CANCEL_FILLED}
                onIconClick={handleUnselectItem}
            />
        ));

    const perPageOptions = [9, '18', 21];

    return (
        <>
            <div className={css(defaultStyle)} ref={divRef}>
                <div className={css(selectedAreaStyle)}>
                    <Button
                        iconEnd={EIconType.ARROW_DOWN}
                        clickHandler={toggleDrop}
                        text={renderLabel()}
                        isLink
                        variation={EButtonVariation.SUBTLE}
                        size={EButtonSize.SMALL}
                    />

                    <Dropdown
                        handleClose={toggleDrop}
                        actionRef={divRef}
                        isOpen={open}
                        headerTitle='test'
                    >
                        <div className={css(dropdownRootStyles)}>
                            <div className={css(selectedTagColumn)}>
                                {renderSelectedTags()}
                            </div>
                            <div
                                className={css(searchContainer)}
                                onBlur={handleBlurSearch}
                            >
                                <Search
                                    searchValue={searchValue}
                                    setSearchValue={setSearchValue}
                                    style={searchStyles}
                                />
                            </div>
                            <div className={css(optionStylesContainer)}>
                                <div className={css(optionsStyles)}>
                                    {renderSelectAll()}
                                    {renderFilteredOptions()}
                                </div>
                                <div className={css(paginationContainer)}>
                                    <Paginator
                                        total={data.length}
                                        rowsPerPageOptions={perPageOptions}
                                        onPageChange={() => {}}
                                        onRowsPerPageChange={() => {}}
                                    />
                                </div>
                            </div>
                            <div className={css(optionsDropdownFooter)}>
                                <Button
                                    variation={EButtonVariation.SECONDARY}
                                    text='Clear All'
                                    clickHandler={handleClearAll}
                                    customWidth={141}
                                    customHeight={40}
                                />
                                <Button
                                    loadingProgress={27}
                                    text='Apply'
                                    clickHandler={handleApplyAll}
                                    customWidth={77}
                                    customHeight={40}
                                />
                            </div>
                        </div>
                    </Dropdown>
                </div>
            </div>
        </>
    );
}

export default MetricDropdownSelection;
