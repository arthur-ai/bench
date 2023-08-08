import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { GRAPHIK } from 'resources/fonts';

export const styles = {
    tooltipDate: {
        marginBottom: '10px',
        fontSize: '12px',
    },
    tooltipDatapoint: {
        fontSize: '14px',
        color: primary.eggplant,
        fontFamily: GRAPHIK,
    },
    tooltipDatapointLabel: {
        color: secondary.variant.eggplant.light,
    },
    tooltipDataColor: {
        display: 'inline-block',
        marginRight: '8px',
        width: '8px',
        height: '8px',
        borderRadius: '8px',
    },
};
