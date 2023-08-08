import React from 'react';
import { useFela } from 'react-fela';
import { TableProps } from './typings';

function Table(props: TableProps) {
    const { css } = useFela();
    const tableStyle: React.CSSProperties = {
        borderSpacing: '1px',
        ...(props.style ? props.style : {}),
    };

    return (
        <table
            data-testid={props.testId || 'table'}
            className={`${props.className || ''} ${css(tableStyle)}`}
        >
            {props.children}
        </table>
    );
}

export default Table;
