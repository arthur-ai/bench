import React, { useRef, useState } from 'react';
import { useFela } from 'react-fela';
import secondary from 'resources/colors/Arthur/secondary';
import useOnClickOutside from 'api/useOnClickOutside';
import { Button, EButtonVariation } from '../../core/Button';
import Icon, { EIconType } from '../../core/Icon';
import PopUp from '../../core/PopUp/PopUp';
import styles from './styles'
import {TSelectItem} from "../../core/StyledSelect/StyledSelect";


type Props = {
    setSortColumn: (arg: string) => void;
    sortOptions: TSelectItem[]

};

const SortDropdown = (props: Props) => {
    const [isOpen, setIsOpen] = useState(false);
    const { css } = useFela();
    const { setSortColumn, sortOptions } = props;
    const [selected, setSelected] = useState(sortOptions[0].id);

    const selectRef = useRef<HTMLDivElement>(null);

    useOnClickOutside(selectRef, () => setIsOpen(false));

    const toggle = () => {
        setIsOpen((prev) => !prev);
    };
    const handleSort = (id: string) => {
        setSelected(id);
        setSortColumn(id);
        setIsOpen(false);
    };
    const getStyles = (id: string) => {
        if (id == selected) {
            return css(styles.option['& selected']);
        }
        return css(styles.option);
    };

    return (
        <div className={css(styles.wrapper)} ref={selectRef}>
            <Button
                text='SORT'
                iconStart={EIconType.SORT_DEFAULT}
                isLink
                variation={EButtonVariation.SUBTLE}
                clickHandler={toggle}
            ></Button>
            <PopUp showPopUp={isOpen} styles={styles.body} customMinHeight={60} setShowPopUp={setIsOpen}>
                <ul className={css(styles.list)}>
                    {sortOptions.map((item) => (
                        <li
                            key={item.id}
                            className={getStyles(item.id)}
                            onClick={() => handleSort(item.id)}
                        >
                            {item.name}
                            {item.id === selected && (
                                <Icon
                                    size={16}
                                    icon={EIconType.SUCCESS}
                                    color={secondary.blue}
                                />
                            )}
                        </li>
                    ))}
                </ul>
            </PopUp>
        </div>
    );
};

export default SortDropdown;
