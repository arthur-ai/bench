import { GRAPHIK } from 'resources/fonts';
import primary from 'resources/colors/Arthur/primary';

import { EChipTheme } from './types';

const chipThemeColors: Record<string, string> = {
    [EChipTheme.ARTHUR]: primary.purple,
}

const styles = (chipTheme: EChipTheme , isMinimal?: boolean) => ({
    root: {
        whiteSpace: 'nowrap',
        fontFamily: GRAPHIK,
        fontSize: '12px',
        backgroundColor: chipTheme !== EChipTheme.DEFAULT ? 'transparent' : primary.ashGrey,
        ...(chipTheme !== EChipTheme.DEFAULT && {
            border: `1px solid ${primary.ashGrey}`,
        }),
        borderRadius: '2px',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: isMinimal ? '0 4px' : '4px 8px',
        color: chipThemeColors[chipTheme] || primary.eggplant,
    },
    button: {
        width: 'auto',
        padding: '0 !important',
    },
    icon: {
        marginLeft: '4px',

        '& path': {
            fill: chipThemeColors[chipTheme] || 'inherit !important',
        },
    },
    name: {
        overflow: 'hidden',
        textOverflow: 'ellipsis',
    },
    iconStart: {
        marginLeft: '0px',
        marginRight: '4px',
    },
});

export default styles;
