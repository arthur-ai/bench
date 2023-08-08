import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { MONO } from 'resources/fonts';
import { ETabsStyle } from './Tabs';

export const tabStyles = {
    root: (style?: ETabsStyle) => ({
        padding: style === ETabsStyle.BUTTONS ? '4px 8px' : '16px',
        whiteSpace: 'nowrap',
        display: 'inline-block',
        cursor: 'pointer',
        ...(style === ETabsStyle.BUTTONS && {
            margin: '3px',
            borderRadius: '2px',
            opacity: 0.6,
        }),
        '&:hover': {
            ...(style === ETabsStyle.BUTTONS
                ? {
                      backgroundColor: secondary.variant.grey.light,
                  }
                : {
                      boxShadow: 'inset 0px -4px 0px 0px rgba(181,54,251,0.5)',
                  }),
        },
    }),
    selected: (theme: any, style?: ETabsStyle) => ({
        pointerEvents: 'none',
        ...(style === ETabsStyle.BUTTONS
            ? {
                  backgroundColor: 'white',
                  fontWeight: 'bold',
                  opacity: 1,
                  boxShadow: '0px 1px 5px rgba(0, 0, 0, 0.1)',
              }
            : {
                  boxShadow: `inset 0px -4px 0px 0px ${theme.color_1}`,
              }),
    }),
    disabled: (style?: ETabsStyle) => ({
        opacity: 0.5,
        pointerEvents: 'none',
        '&:hover': {
            ...(style !== ETabsStyle.BUTTONS && {
                boxShadow: `inset 0px -4px 0px 0px ${primary.ashGrey}`,
            }),
        },
    }),
};

export default {
    root: (style?: ETabsStyle) => ({
        overflowY: 'hidden',
        whiteSpace: 'nowrap',
        color: primary.eggplant,
        textTransform: 'uppercase',
        fontFamily: MONO,
        letterSpacing: '0.05em',
        fontWeight: 500,
        fontSize: '12px',
        ...(style === ETabsStyle.BUTTONS && {
            backgroundColor: secondary.variant.grey.active,
            borderRadius: '2px',
            border: '1px solid #E8E8ED',
            fontWeight: 400,
        }),
    }),
};
