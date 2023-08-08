import React, { useEffect, useState } from 'react';
import { useFela } from 'react-fela';
import styles from './Toggle.styles';
import { ToggleProps } from './Toggle.types';

const Toggle = (props: ToggleProps) => {
    const { isActive, toggleIsActive, height, width, outlined, disabled } =
        props;
    const { css } = useFela({ isActive, height, width, outlined, disabled });
    const [localActive, setLocalActive] = useState(isActive);

    useEffect(() => setLocalActive(isActive), [isActive]);

    const handleChange = (e: React.MouseEvent<HTMLLabelElement>) => {
        if (disabled || typeof toggleIsActive !== 'function') {
            return;
        }

        e.preventDefault();
        toggleIsActive(!localActive);
    };

    return (
        <label
            role='presentation'
            className={css(styles.switch)}
            onClick={handleChange}
        >
            <input
                checked={localActive}
                disabled={disabled}
                className={css(styles.checkbox)}
                type='checkbox'
                tabIndex={disabled || !toggleIsActive ? -1 : 0}
            />
            <span className={css(styles.slider)} data-slider />
        </label>
    );
};

export default Toggle;
