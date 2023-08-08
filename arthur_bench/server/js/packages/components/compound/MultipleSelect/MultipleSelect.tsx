import React, { useRef, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import Icon, { EIconType } from '@core/Icon';
import { Button, EButtonSize } from '@core/Button';
import { useFela } from 'react-fela';
import styles from './styles';
import Chip, { TChip, EChipTheme } from '../Chip';
import { TThemeType } from 'resources/theme/types';
import Dropdown from '@core/Dropdown';
import secondary from 'resources/colors/Arthur/secondary';
import useOnClickOutside from "api/useOnClickOutside";

type TChips = TChip[];

export type TChipSelectorProps = {
    onChange: (selectedChips: TChips) => void;
    chips: TChips;
    selectedChips: TChips;
    onCreateNew?: (chip: TChip) => void;
    placeHolder?: string;
    isInline?: boolean;
    dropDownZIndex?: number;
    preventCloseOnOutsideClick?: boolean;
    isOpen: boolean;
    setIsOpen: (arg0: boolean) => void;
    modelId?: string;
    handleDelete?: (id: string, modelId: string) => void;
};

const MultipleSelect: React.FC<TChipSelectorProps> = (
    props: TChipSelectorProps
): React.ReactElement<TChipSelectorProps> => {
    const {
        chips,
        onChange,
        selectedChips,
        onCreateNew,
        placeHolder,
        isInline,
        isOpen,
        setIsOpen,
        handleDelete,
        modelId,
        preventCloseOnOutsideClick,
    } = props;
    const [searchValue, setSearchValue] = useState<string>('');
    const [showDropdown, setShowDropDown] = useState(false);
    const { css, theme } = useFela<TThemeType>();
    const classNames = styles(isOpen, theme, isInline);
    const inputRef: React.RefObject<HTMLInputElement> =
        useRef<HTMLInputElement>(null);
    const chipsHolderRef: React.RefObject<HTMLDivElement> =
        useRef<HTMLDivElement>(null);

    useOnClickOutside(chipsHolderRef, () => {
        if (!preventCloseOnOutsideClick) {
            setIsOpen(false);
        }
    });

    const handleRemoveChip = (chip: TChip) => {
        const result = selectedChips.filter((t) => t.id !== chip.id);
        onChange(selectedChips.filter((t) => t.id !== chip.id));
        handleDelete && modelId && handleDelete(chip.id, modelId);
        if (!result.length) {
            setIsOpen(false);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchValue(e.target.value);
    };

    const handleInputBlur = (event: React.FocusEvent<HTMLInputElement>) => {
        const relatedTarget = event.relatedTarget as HTMLElement;
        const isOptionClicked =
            relatedTarget && relatedTarget.dataset?.attr === 'select-option';

        if (!isOptionClicked) {
            setShowDropDown(false);

            if (!selectedChips.length) {
                setIsOpen(false);
            }
        }
    };

    const renderChips = () =>
        selectedChips.map((chip) => (
            <Chip
                theme={EChipTheme.ARTHUR}
                iconEnd={EIconType.CANCEL}
                overrideStyles={classNames.chip}
                onIconClick={handleRemoveChip}
                chip={chip}
            />
        ));

    const handleAddChip = (chip: TChip) => {
        onChange([...selectedChips, chip]);
        setSearchValue('');
        setShowDropDown(false);

        if (chipsHolderRef.current) {
            chipsHolderRef.current.scroll({
                left: chipsHolderRef.current.scrollWidth,
            });
        }
    };

    const handleCloseDropDown = () => {
        setShowDropDown(false);
    };

    const createNewChip = () => {
        const id = uuidv4();
        const chip = { name: searchValue, id };
        handleAddChip(chip);
        onCreateNew && onCreateNew(chip);
    };

    const chipExists = () =>
        chips.some(
            (tag) => tag.name.toLowerCase() === searchValue.toLowerCase()
        );

    const renderDropdown = () => {
        const filteredChips = searchValue
            ? chips.filter(
                  (t) =>
                      t.name
                          .toLowerCase()
                          .includes(searchValue.toLowerCase()) &&
                      !selectedChips.includes(t)
              )
            : chips.filter((t) => !selectedChips.includes(t));
        const canCreateNewChip =
            (!filteredChips.length || !chipExists()) &&
            !!searchValue &&
            onCreateNew;

        return (
            <Dropdown
                inlineStyles={{ zIndex: props.dropDownZIndex }}
                actionRef={inputRef}
                isOpen={showDropdown}
                handleClose={handleCloseDropDown}
            >
                <div id='dropdown' className={css(classNames.dropdown)}>
                    {filteredChips.length ? (
                        filteredChips.map((t: TChip) => (
                            <div
                                data-attr='select-option'
                                tabIndex={0}
                                role='button'
                                onMouseUp={() => handleAddChip(t)}
                                key={t.id}
                                className={css(classNames.dropdownItem)}
                            >
                                {t.name}
                            </div>
                        ))
                    ) : (
                        <div className={css(classNames.dropdownItem)}>
                            No Tags Found
                        </div>
                    )}
                    {canCreateNewChip && (
                        <div
                            className={css(
                                classNames.dropdownItem,
                                classNames.addNew
                            )}
                            data-attr='select-option'
                            tabIndex={0}
                            role='button'
                            onMouseUp={createNewChip}
                        >
                            <span className={css(classNames.addNewTitle)}>
                                Create
                            </span>
                            {searchValue}
                        </div>
                    )}
                </div>
            </Dropdown>
        );
    };

    const handleClearAll = () => {
        onChange([]);
        setIsOpen(false);
    };

    const handleInputFocus = () => {
        setShowDropDown(true);
    };

    const getPlaceholder = () => (selectedChips.length ? '' : placeHolder);

    return (
        <div className={css(classNames.root)}>
            {isOpen && (
                <>
                    <div
                        ref={chipsHolderRef}
                        className={css(classNames.chipsHolder)}
                    >
                        {renderChips()}
                        <input
                            onFocus={handleInputFocus}
                            onBlur={handleInputBlur}
                            className={css(classNames.input)}
                            ref={inputRef}
                            placeholder={getPlaceholder()}
                            type='text'
                            value={searchValue}
                            onChange={handleInputChange}
                        />
                        {renderDropdown()}
                    </div>
                    {!!selectedChips.length && (
                        <Button
                            className={css(classNames.clearButton)}
                            clickHandler={handleClearAll}
                            isLink
                            text='Clear all'
                            size={EButtonSize.SMALL}
                        />
                    )}
                    {selectedChips.length == 0 && (
                        <Icon
                            clickHandler={() => setIsOpen(false)}
                            className={css(classNames.inputClear)}
                            icon={EIconType.CANCEL_FILLED}
                            size={14}
                            color={secondary.blue}
                        />
                    )}
                </>
            )}
        </div>
    );
};

export default MultipleSelect;
