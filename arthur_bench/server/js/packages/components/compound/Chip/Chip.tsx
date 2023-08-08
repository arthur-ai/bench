import React from 'react';
import { useFela } from 'react-fela';

import Icon from '@core/Icon';
import { Button, EButtonSize } from '@core/Button';

import styles from './styles';
import { EChipTheme, TChipProps } from './types';

const Chip: React.FC<TChipProps> = (
    props: TChipProps
): React.ReactElement<TChipProps> => {
    const {
        chip,
        theme = EChipTheme.DEFAULT,
        chipName,
        minimal,
        iconEnd,
        iconStart,
        onIconClick,
        overrideStyles = {},
        iconStartColor
    } = props;

    const className = styles(theme, minimal);
    const { css } = useFela();

    const iconClickHandler = () => {
        if (onIconClick && chip) {
            onIconClick(chip);
        }
    };

    const renderStartIcon = () => {
        if (iconStart) {
            return (
                <Icon
                    className={css(className.icon, className.iconStart)}
                    size={16}
                    icon={iconStart}
                    color={iconStartColor}
                />
            );
        }
    };

    const renderEndIcon = () => {
        if (iconEnd && onIconClick) {
            return (
                <Button
                    iconSize={16}
                    iconClass={css(className.icon)}
                    className={css(className.button)}
                    iconEnd={iconEnd}
                    size={EButtonSize.SMALL}
                    isLink
                    clickHandler={iconClickHandler}
                />
            );
        } else if (iconEnd) {
            return (
                <Icon className={css(className.icon)} size={16} icon={iconEnd} />
            );
        }

        return null;
    };

    return (
        <div className={`${css(className.root, overrideStyles)}`}>
            {renderStartIcon()}
            <span className={css(className.name)}>{chip ? chip.name : ''}</span>
            {chipName ? chipName : ''}
            {renderEndIcon()}
        </div>
    );
};

export default Chip;
