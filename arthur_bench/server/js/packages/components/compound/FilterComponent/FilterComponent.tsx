import React from 'react';
import { connect as connectStyles } from 'react-fela';
import { compose } from 'ui/helpers/compose';
import { useFela } from 'react-fela';
import Checkbox from '../../core/Checkbox';
import Field from '../../core/Field';
import Icon from '../../core/Icon';
import styles from './FilterComponent.styles';
import { FilterComponentProps } from './FilterComponentProps.types';

const FilterComponent = ({
    icon,
    label,
    type = 'horizontal',
    isActive = false,
    clickHandler = () => {},
    styles = {},
    color,
}: FilterComponentProps) => {
    const { theme }: any = useFela();

    return (
        <div className={styles.wrap}>
            {icon && (
                <div className={styles.icon}>
                    <Icon icon={icon} size={35} color={theme.color_1} />
                </div>
            )}
            {type === 'selection' && (
                <div onClick={clickHandler} role='presentation'>
                    <Checkbox
                        clickHandler={clickHandler}
                        checked={isActive}
                        color={color ? color : theme.color_1}
                    />
                </div>
            )}
            <div className={styles.label}>
                <Field label={label} />
            </div>
        </div>
    );
};

export default compose(connectStyles(styles))(FilterComponent);
