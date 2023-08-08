import React, {useRef, useState} from 'react';
import { useFela } from 'react-fela';
import secondary from 'resources/colors/Arthur/secondary';
import { TThemeType } from 'resources/theme/types';
import FilterButton from '@compound/FilterButton/FilterButton';
// import { Button, EButtonSize, EButtonVariation } from '../Button'
import Icon, { EIconType } from '../Icon';
import styles from './Search.styles';
import { SearchProps, ESearchVariations } from './types';
import useOnClickOutside from "api/useOnClickOutside";

const Search = ({
    searchValue,
    setSearchValue,
    style = {},
    variation = ESearchVariations.NORMAL,
    text,
}: SearchProps) => {
    const [isActive, setIsActive] = useState(false);

    const { css, theme } = useFela<TThemeType>();
    const classNames = styles(isActive, theme, variation);
    const searchRef = useRef<HTMLDivElement>(null);

    useOnClickOutside(searchRef, () => setIsActive(false));

    return (
        <div className={css([classNames.wrap, style])} ref={searchRef}>
            {isActive ? (
                <div className={css(classNames.inputWrap)}>
                    <input
                        className={css(classNames.input)}
                        placeholder={text || 'Search'}
                        type='text'
                        value={searchValue}
                        onChange={(e) => setSearchValue(e.target.value)}
                    />
                    <Icon
                        clickHandler={() => {
                            setIsActive(false);
                            setSearchValue('');
                        }}
                        className={css(classNames.inputClear)}
                        icon={EIconType.CANCEL_FILLED}
                        size={14}
                        color={secondary.blue}
                    />
                </div>
            ) : (
                <FilterButton
                    text={text || 'Search'}
                    icon={EIconType.SEARCH}
                    onClick={() => setIsActive(true)}
                />
            )}
        </div>
    );
};

export default Search;
