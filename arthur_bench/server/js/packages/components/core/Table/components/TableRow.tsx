import React, { useEffect, useRef, useState } from 'react';
import { useFela } from 'react-fela';
import { TableRowProps } from '../typings';
import { closedRow, defaultRowStyle, openRow } from '../styles';

function TableRow(props: TableRowProps) {
    const { css } = useFela();
    const { open = true, testId = 'table-row' } = props;

    const combinedStyle = {
        ...(props.onClick ? { cursor: 'pointer' } : {}),
        ...defaultRowStyle,
        ...(open ? openRow : closedRow),
        ...(props.style ?? {})
    };

    return (
        <tr
            data-testid={testId}
            className={`${props.className || ''} ${css(combinedStyle)}`}
            onClick={props.onClick ? props.onClick : undefined}
            tabIndex={props.onClick ? 0 : undefined}
            {...props}
        >
            {props.children}
        </tr>
    );
}

export default TableRow;
