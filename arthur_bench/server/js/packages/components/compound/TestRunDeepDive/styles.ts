import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import {GRAPHIK_LIGHT, MONO, MONO_MEDIUM} from 'resources/fonts';

const styles = {
    headerCell: (color: string) => ({
        backgroundColor: color,
        fontFamily: MONO_MEDIUM,
        border: `1px solid ${primary.ashGrey}`,
        textAlign: 'left',
    }),
    table: {
        borderCollapse: 'collapse',
        border: `1px solid ${primary.ashGrey}`,
    },
    cell: (width?: string) => ({
        border: `1px solid ${primary.ashGrey}`,
        fontSize: '16px',
        FontFamily: GRAPHIK_LIGHT,
        textAlign: 'left',
        padding: '16px',
        width: width ?? 'auto'
    }),
};

export default styles;
