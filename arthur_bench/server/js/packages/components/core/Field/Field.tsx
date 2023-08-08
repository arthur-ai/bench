import React from 'react';
import { useFela } from 'react-fela';
import styles from './Field.styles';
import { FieldProps } from './types';

const Field = ({ label, sublabel }: FieldProps) => {
    const { css } = useFela();

    return (
        <div className={css(styles.field)}>
            <p className={css(styles.fieldLabel)}>{label}</p>
            {Boolean(sublabel) && (
                <p className={css(styles.fieldSublabel)}>{sublabel}</p>
            )}
        </div>
    );
};

export default Field;
