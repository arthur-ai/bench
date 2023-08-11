import React from 'react';
import { useFela } from 'react-fela';
import styles from './Checkbox.styles';
import { CheckboxProps } from './typings';

const Checkbox = (props: CheckboxProps) => {
    const { clickHandler, checked, label, color } = props;
    const { css, theme } = useFela();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        clickHandler && clickHandler(e.target.checked);
    };

    return (
        <label className={css(styles.root)}>
            <div className={css(styles.checkboxWrap)}>
                <input
                    onChange={handleChange}
                    checked={checked}
                    type='checkbox'
                    className={css(styles.checkbox(theme, color))}
                    data-testid={props.testId || 'checkbox'}
                />
                {checked && <span className={css(styles.icon(theme, color))} />}
            </div>
            {label ? <div className={css(styles.label)}>{label}</div> : null}
        </label>
    );
};

export default Checkbox;
