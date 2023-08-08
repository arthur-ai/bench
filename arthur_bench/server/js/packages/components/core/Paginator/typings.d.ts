import React, { HTMLAttributes, FunctionComponent } from 'react';

export interface PaginatorProps extends HTMLAttributes<FunctionComponent> {
    complex?: boolean;
    disabled?: boolean;
    allowPageInput?: boolean;
    onPageChange: (page: number) => void;
    onRowsPerPageChange?: (perPage: number) => void;
    page?: number | string;
    rowsPerPage?: number;
    rowsPerPageOptions?: Array[number | string];
    total: number;
    zeroTotalMessage?: string;
}

export interface PaginatorState {
    openDrop: boolean;
    page: number;
    perPage: number;
    perPageOpts: number[];
}
