import React from 'react';
import { useFela } from 'react-fela';
import { TableCellProps } from '../typings';
import { defaultCellStyle, scrollableCell } from '../styles';

function TableCell(props: TableCellProps) {
    const { css, theme } = useFela();
    const {
        span = 1,
        // @ts-ignore
        // backgroundColor = theme?.bkg_2 || '#FFFFFF',
        // @ts-ignore
        color = theme?.color || '#000000',
        boxShadow = 'inset 0px -1px 0px rgba(26, 0, 22, 0.1)',
        clickHandler,
    } = props;

    const combinedStyle: React.CSSProperties = {
        ...defaultCellStyle,
        // backgroundColor,
        color,
        boxShadow,
        ...(props.style ? props.style : {}),
    };

    // Dynamically choose which cell type to render
    const component = {
        type: (props.headCell ? 'th' : 'td') as React.ElementType,
    };

    return (
        <component.type
            data-testid={
                props.testId || `table-${props.headCell ? 'head' : 'cell'}`
            }
            className={`${props.className || ''} ${css(combinedStyle)}`}
            colSpan={span}
            onClick={clickHandler ? clickHandler : null}
        >
            {props.children ? <div>{props.children}</div> : <span>Empty Cell</span>}
        </component.type>
    );
}

export default TableCell;
