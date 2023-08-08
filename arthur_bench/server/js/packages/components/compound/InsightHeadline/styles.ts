import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { GRAPHIK, GRAPHIK_MEDIUM, GRAPHIK_SEMI } from 'resources/fonts';

export const styles = {
    root: {
        fontFamily: GRAPHIK,
        border: `1px solid ${primary.ashGrey}`,
        padding: '18px',
        cursor: 'pointer',
        borderBottom: 'none',

        '&:last-of-type': {
            borderBottom: `1px solid ${primary.ashGrey}`,
        },
    },
    headlineWrap: {
        display: 'flex',
        alignItems: 'center',

        '> div': {
            marginRight: '16px',
        },
    },
    timestamp: {
        fontSize: '12px',
        marginBottom: '8px',
    },
    message: {
        color: secondary.variant.eggplant.lighter,
        margin: 0,
        fontSize: '14px',

        '> strong': {
            color: primary.eggplant,
            fontFamily: GRAPHIK_MEDIUM,
        },
    },
};
