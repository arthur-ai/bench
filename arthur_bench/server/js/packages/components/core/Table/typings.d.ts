import React from 'react';

export interface TableProps extends React.HTMLAttributes<HTMLTableElement> {
    testId?: string;
}
export interface TableHeaderProps
    extends React.HTMLAttributes<HTMLTableSectionElement> {
    testId?: string;
}
export interface TableBodyProps
    extends React.HTMLAttributes<HTMLTableSectionElement> {
    testId?: string;
}
export interface TableFooterProps
    extends React.HTMLAttributes<HTMLTableSectionElement> {
    testId?: string;
}
export interface TableRowProps
    extends React.HTMLAttributes<HTMLTableRowElement> {
    testId?: string;
    open?: boolean;
}

export interface TableCellProps
    extends React.HTMLAttributes<HTMLTableCellElement> {
    testId?: string;
    backgroundColor?: string;
    color?: string;
    boxShadow?: string;
    headCell?: boolean;
    span?: number;
    clickHandler?: Function;
}
