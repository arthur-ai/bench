import React from 'react';

export const defaultCellStyle: React.CSSProperties = {
    padding: '8px 16px',
    textAlign: 'center',
};

export const scrollableCell= {
    maxHeight: '100px',
    overflow: 'auto',
    margin: '10px 0px'
}

export const defaultRowStyle = {
    width: '100%',
};

export const openRow = {
    '> td': {
        lineHeight: '100%',
        transitionDuration: '0.5s',
    },
};

export const closedRow = {
    '> td': {
        overflow: 'hidden',
        transitionDuration: '0.5s',
        padding: '0px 0px',
        lineHeight: '0px',
        whiteSpace: 'nowrap',
    },
};
