import React, { useRef, useState } from 'react';
import styles from './styles';
import Icon, { EIconType } from '../Icon';
import { useFela } from 'react-fela';
import Dropdown from '../Dropdown';

export type TSelectItem = {
    id: string;
    name: string;
};

/**
 * @param filled Works with styled view only
 * @param large Works with styled view only
 */

type SelectProps<T extends TSelectItem> = {
    items: T[];
    selectedItem?: T | null;
    defaultValueView?: boolean;
    disabled?: boolean;
    filled?: boolean;
    large?: boolean;
    label?: string;
    placeholder?: string;
    className?: any;
    dropDownMaxHeight?: number;
    dropDownZIndex?: number;
    changeHandler: (item: T) => void;
    titleRenderer?: (item: T) => string | Element;
    dropdownWidth?: string;
    customWidth?: number;
    alignedLeft?: boolean;
    customStyles?: any;
};

const StyledSelect = <T extends TSelectItem>(props: SelectProps<T>) => {
    const {
        placeholder,
        className,
        items,
        label,
        defaultValueView,
        selectedItem,
        filled,
        large,
        dropDownMaxHeight = 280,
        disabled,
        titleRenderer,
        dropdownWidth,
        customWidth,
        alignedLeft = false,
        customStyles,
    } = props;
    const { css } = useFela();
    const selectRef = useRef<HTMLDivElement>(null);
    const [isOpen, setIsOpen] = useState(false);

    const toggleOpen = () => setIsOpen(!isOpen);

    const handleChange = (item: T) => {
        toggleOpen();
        props.changeHandler(item);
    };

    const renderValue = () => (
        <div
            className={css(styles.root(disabled), className)}
            ref={selectRef}
            data-testid="styledSelectToggle"
            onMouseDown={toggleOpen}
            tabIndex={-1}
            role='button'
        >
            {defaultValueView ? (
                selectedItem?.name || ''
            ) : (
                <div
                    className={css(
                        styles.select(
                            isOpen,
                            filled,
                            large,
                            customStyles,
                            !!(placeholder && !selectedItem)
                        )
                    )}
                >
                    <>
                        <Icon
                            size={22}
                            className={css(
                                styles.selectIcon(isOpen, large, customStyles)
                            )}
                            icon={EIconType.ARROW_DOWN}
                        />
                        {titleRenderer && selectedItem
                            ? titleRenderer(selectedItem)
                            : selectedItem?.name || placeholder || ''}
                    </>
                </div>
            )}
        </div>
    );

    const renderOptions = () => {
        const isLarge = large && !defaultValueView;
        const width = dropdownWidth || `${selectRef.current?.offsetWidth}px`;

        return (
            <Dropdown
                inlineStyles={{ zIndex: props.dropDownZIndex }}
                isOpen={isOpen}
                handleClose={toggleOpen}
                actionRef={selectRef}
            >
                <div
                    className={css(
                        styles.dropdown(
                            !!isLarge,
                            width,
                            `${dropDownMaxHeight}px`
                        )
                    )}
                >
                    {items.map((i) => (
                        <div
                            key={i.id}
                            className={css(styles.dropdownItem(!!isLarge))}
                            tabIndex={-1}
                            role='button'
                            data-testid='styledSelectOption'
                            onMouseDown={() => handleChange(i)}
                        >
                            {i.name}
                        </div>
                    ))}
                </div>
            </Dropdown>
        );
    };

    const renderLabel = () => {
        return label ? <div className={css(styles.label)}>{label}</div> : null;
    };

    return (
        <div
            data-testid='StyledSelect'
            className={css(styles.container(customWidth, alignedLeft))}
        >
            {renderLabel()}
            {renderValue()}
            {renderOptions()}
        </div>
    );
};

export default StyledSelect;
