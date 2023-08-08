import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { GRAPHIK, MONO } from 'resources/fonts';
import {
    dropdownItemStyles,
    dropdownStyles,
} from '@compound/MultipleSelect/styles';

export default {
    label: {
        marginBottom: '8px',
        fontSize: '12px',
        fontFamily: MONO,
        color: primary.eggplant,
    },
    root: (disabled: boolean | undefined) => ({
        fontSize: '14px',
        fontFamily: GRAPHIK,
        cursor: disabled ? 'default' : 'pointer',
        ...(disabled && {
            opacity: '0.5',
            pointerEvents: 'none',
        }),
    }),
    container: (
        customWidth: number | undefined,
        alignedLeft: boolean = false
    ) => ({
        width: `${customWidth}px`,
        ...(alignedLeft ? { textAlign: 'left' } : {}),
    }),
    selectIcon: (
        isOpen: boolean,
        large: boolean | undefined,
        customStyles?: any
    ) => ({
        pointerEvents: 'none',
        position: 'absolute',
        right: large ? '8px' : '4px',
        top: large ? '8px' : '4px',
        fill: customStyles?.fill,
        transition: '0.3s',
        ...(isOpen && { transform: 'rotate(180deg)' }),
    }),
    select: (
        isOpen: boolean,
        filed: boolean | undefined,
        large: boolean | undefined,
        customStyles?: Record<string, string>,
        placeholder?: boolean
    ) => ({
        position: 'relative',
        width: '100%',
        boxSizing: 'border-box',
        borderRadius: '2px',
        padding: large ? '11.5px 40px 11.5px 11.5px' : '8px 30px 8px 8px',
        border: `1px solid ${isOpen ? secondary.blue : primary.ashGrey}`,
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        ...(filed && {
            backgroundColor: customStyles?.backgroundColor || primary.white,
            boxShadow: '0px 1px 5px rgba(0, 0, 0, 0.1)',
            color: customStyles?.color,
            fontFamily: customStyles?.fontFamily,
            letterSpacing: customStyles?.letterSpacing,
        }),
        ...(placeholder && {
            color: 'gray',
        }),
    }),
    dropdown: (large: boolean, width: string, maxHeight: string) => ({
        ...dropdownStyles,
        ...(large && { width }),
        maxHeight,
        overflow: 'auto',
        display: 'flex',
        flexDirection: 'column'
    }),
    dropdownItem: (large: boolean) => ({
        ...dropdownItemStyles,
        ...(large && { padding: '16px' }),
        fontSize: '14px',
    }),
};
