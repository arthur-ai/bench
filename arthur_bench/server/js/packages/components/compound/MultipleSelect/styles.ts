import { TThemeType } from 'resources/theme/types';
import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { MONO, GRAPHIK } from 'resources/fonts';

export const dropdownStyles = {
    backgroundColor: primary.white,
    boxShadow: '0px 4px 8px rgba(26, 0, 22, 0.1)',
    borderRadius: '2px',
    fontSize: '12px',
    fontFamily: GRAPHIK,
    color: primary.eggplant,
};

export const dropdownItemStyles = {
    padding: '8px',
    cursor: 'pointer',
    ':hover': {
        backgroundColor: secondary.lightBlue,
    },
};

const styles = (isOpen: boolean, theme: TThemeType, isInline?: boolean) => ({
    root: {
        justifyContent: 'space-between',
        position: 'relative',
        display: 'flex',
        lineHeight: '1',
        alignItems: 'center',
        borderRadius: '4px',
        padding: '4px 0 4px 4px',
        height: 'auto',
        ...(isOpen && {
            width: '380px',
            backgroundColor: theme.tagSelector.backgroundColor,
            border: '1px solid #2D78CB',
        }),
        ...(isInline && {
            height: '22px',
        }),
    },
    chip: {
        margin: '4px',
    },
    chipsHolder: {
        width: '100%',
        display: 'flex-wrap',
        overflowX: 'auto',
        '-ms-overflow-style': 'none',
        scrollbarWidth: 'none',
        '&::-webkit-scrollbar': {
            display: 'none',
        },
        ...(isInline && { display: 'flex' }),
    },
    clearButton: {
        marginLeft: 'auto',
        marginRight: '8px',
        width: 'auto',
        padding: '8px !important',
        textDecoration: 'none !important',
    },
    inputClear: {
        padding: '8px !important',
        cursor: 'pointer',
    },
    icon: {
        margin: '0 4px',
    },
    button: {
        color: `${primary.eggplant} !important`,
        borderRadius: '4px',
        transition: '0.5s',
        padding: '8px !important',
        '&:hover': {
            textDecoration: 'none !important',
            backgroundColor: 'white !important',
        },
        '& path': {
            transition: '0.5s',
            fill: `${primary.eggplant} !important`,
        },
    },
    input: {
        width: '100%',
        minWidth: '110px',
        fontFamily: MONO,
        textTransform: 'uppercase',
        fontSize: '12px',
        letterSpacing: '0.05em',
        backgroundColor: 'transparent',
        border: '0',
        '&:focus': {
            outline: 'none',
            border: '0',
        },
    },
    dropdown: {
        ...dropdownStyles,
    },
    dropdownItem: {
        ...dropdownItemStyles,
    },
    addNew: {
        maxWidth: '150px',
        textOverflow: 'ellipsis',
        overflow: 'hidden',
        white: 'no-wrap',
    },
    addNewTitle: {
        color: primary.eggplant,
        opacity: 0.5,
        marginRight: '4px',
    },
});

export default styles;
