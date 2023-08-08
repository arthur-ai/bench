import React from 'react';
import primary from 'resources/colors/Arthur/primary';

const commonBox: React.CSSProperties = {
    background: 'none',
    border: '2px solid #E4E0E4',
    color: 'black',
    height: '32px',
};

export const defaultStyle: React.CSSProperties = {
    display: 'inline-flex',
    background: 'none',
    height: '32px',
};

export const textAlign: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
};

export const rowsPerPageStyles: React.CSSProperties = {
    display: 'inline-flex',
};

export const morePage: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '4px',
    minWidth: '32px',
    height: '32px',
    color: primary.raisin,
    boxSizing: 'border-box',
    cursor: 'pointer',
};

export const currentPageStyles: React.CSSProperties = {
    backgroundColor: primary.purple,
    color: primary.white,
};

export const pages: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
};

export const pageInputWrap: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginLeft: '8px',
};

export const pageInput = {
    border: `1px solid ${primary.ashGrey}`,
    borderRadius: `2px`,
    width: `64px`,
    padding: '7.5px',
    boxSizing: 'border-box',
    backgroundColor: 'inherit',
    '&:focus': {
        outline: 'none',
        borderColor: primary.purple,
    },
};

export const dropdownToggleStyle: React.CSSProperties = {
    ...commonBox,
    boxShadow: 'none',
    minWidth: '52px',
    padding: '3px',
    display: 'flex',
    alignContent: 'center',
};

export const dropdownStyle: React.CSSProperties = {
    border: `1px solid ${primary.ashGrey}`,
    zIndex: 999,
};

export const dropdownButtonStyle: React.CSSProperties = {
    display: 'block',
    margin: 0,
    backgroundColor: 'inherit',
    border: 'none',
    minWidth: '52px',
    height: '32px',
    cursor: 'pointer',
};

export const pageButtonStyle: React.CSSProperties = {
    ...commonBox,
    boxShadow: 'none',
    background: 'none',
    height: '32px',
    minWidth: '32px',
    maxWidth: '44px',
    padding: '0px, 8px, 0px, 8px',
};
