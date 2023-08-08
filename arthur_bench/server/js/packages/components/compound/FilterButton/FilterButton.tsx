import React, { ForwardedRef } from 'react';
import { Button, EButtonSize } from '@core/Button';
import { useFela } from 'react-fela';
import styles from './styles';
import { EIconType } from '@core/Icon/types';

export type FilterButtonProps = {
    text: string;
    icon: EIconType;
    isActive?: boolean;
    onClick: () => void;
};

const FilterButton = React.forwardRef(
    (props: FilterButtonProps, ref: ForwardedRef<HTMLButtonElement>) => {
        const { css } = useFela();
        const classNames = styles(props.isActive);

        return (
            <Button
                size={EButtonSize.SMALL}
                clickHandler={props.onClick}
                className={css(classNames.root)}
                isLink
                ref={ref}
                text={props.text}
                iconStart={props.icon}
            />
        );
    }
);

FilterButton.displayName = 'ArthurFilterButton';

export default FilterButton;
