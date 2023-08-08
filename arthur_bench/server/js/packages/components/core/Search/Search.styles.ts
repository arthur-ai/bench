import { TThemeType } from 'resources/theme/types';
import { ESearchVariations, TSearchVariations } from './types';
import { MONO } from 'resources/fonts';
import primary from 'resources/colors/Arthur/primary';

const styles = (
    isActive: boolean,
    theme: TThemeType,
    variation: TSearchVariations
) => ({
    wrap: {
        boxSizing: 'border-box',
        justifyContent: 'space-between',
        position: 'relative',
        display: 'flex',
        lineHeight: '1',
        alignItems: 'center',
        borderRadius: '4px',
        height: '32px',
        padding: `4px 0 4px ${isActive ? '4px' : '0'}`,
        width: variation === ESearchVariations.NORMAL ? 'auto' : '250px',
        ...(isActive && {
            width: '250px',
            backgroundColor: theme.tagSelector.backgroundColor,
            border:
                variation === ESearchVariations.NORMAL
                    ? `1px solid #2D78CB`
                    : '',
        }),
    },
    inputWrap: {
        display: 'flex',
        width: '100%',
        paddingRight: '5px',
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
    inputClear: {
        cursor: 'pointer',
    },
    searchButton: {
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
});

export default styles;
