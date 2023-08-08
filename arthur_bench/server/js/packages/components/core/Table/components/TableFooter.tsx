import React from 'react';
import { useFela } from 'react-fela';
import { TableFooterProps } from '../typings';

function TableFooter(props: TableFooterProps) {
    const { css } = useFela();
    return (
        <tfoot
            data-testid={props.testId || 'table-foot'}
            className={`${props.className || ''} ${css({
                ...(props.style ? props.style : {}),
            })}`}
        >
            {props.children}
        </tfoot>
    );
}

export default TableFooter;
