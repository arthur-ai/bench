import React from 'react';
import { useFela } from 'react-fela';
import { TableBodyProps } from '../typings';

function TableBody(props: TableBodyProps) {
    const { css } = useFela();
    return (
        <tbody
            data-testid={props.testId || 'table-body'}
            className={`${props.className || ''} ${css({
                ...(props.style ? props.style : {}),
            })}`}
        >
            {props.children}
        </tbody>
    );
}

export default TableBody;
