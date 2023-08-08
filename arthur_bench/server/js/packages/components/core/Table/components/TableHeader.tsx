import React from 'react';
import { useFela } from 'react-fela';
import { TableHeaderProps } from '../typings';

function TableHeader(props: TableHeaderProps) {
    const { css } = useFela();
    return (
        <thead
            data-testid={props.testId || 'table-head'}
            className={`${props.className || ''} ${css({
                ...(props.style ? props.style : {}),
            })}`}
        >
            {props.children}
        </thead>
    );
}

export default TableHeader;
