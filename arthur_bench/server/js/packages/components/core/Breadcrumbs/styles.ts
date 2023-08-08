import primary from 'resources/colors/Arthur/primary';
import { MONO } from 'resources/fonts';

export default {
    root: {
        fontFamily: MONO,
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        fontSize: '12px',
        fontStyle: 'normal',
        fontWeight: 400,
        lineHeight: '24px',
    },
    item: {
        display: 'flex',
        alignItems: 'center',
    },
    divider: {
        color: primary.raisin,
        marginLeft: '5px',
        marginRight: '5px',
        fontWeight: 500,
        fontSize: '14px',
        lineHeight: '14px',
    },
    link: {
        color: primary.eggplant,
        textDecoration: 'none',
        opacity: 0.7,
        whiteSpace: 'nowrap',
        '&:hover': {
            opacity: 1,
        },
    },
    label: (isLast: boolean) => ({
        color: primary.eggplant,
        whiteSpace: 'nowrap',
        opacity: isLast ? 1 : 0.7,
    }),
};
