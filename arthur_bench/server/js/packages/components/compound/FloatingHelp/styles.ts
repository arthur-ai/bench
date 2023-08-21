import { FelaStyle } from 'react-fela';
import primary from 'resources/colors/Arthur/primary';
import { GRAPHIK, MONO } from 'resources/fonts';

export const iconStyle: FelaStyle<any, any> = {
    color: 'white',
    cursor: 'pointer',
    position: 'fixed',
    right: '40px',
    bottom: '110px',
    zIndex: 11,
};

export const panelStyle = (open: boolean): FelaStyle<any, any> => ({
    display: open ? 'block' : 'none',
    height: 'auto', //'917px',
    maxWidth: '919px',
    width: '919px',
    backgroundColor: '#FFFFFF',
    boxShadow: '0px 4px 12px rgba(26, 0, 22, 0.1)',
    borderRadius: '2px',
    position: 'fixed',
    right: '3%',
    bottom: '15%',
    zIndex: 11,
});

export const headerStyle: FelaStyle<any, any> = {
    width: '100%',
    height: '48px',
    borderRadius: '2px 2px 0px 0px',
    boxShadow: 'inset 0px -1px 0px rgba(26, 0, 22, 0.1)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '12px',
    boxSizing: 'border-box',
    '> div': {
        fontFamily: MONO,
        fontWeight: 500,
        fontSize: '14px',
        lineHeight: '40px',
        letterSpacing: '5%',
        color: primary.eggplant,
    },
};

export const iconBox = {
    height: '40px',
    width: '40px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: '10px',
};

export const contentStyle: FelaStyle<any, any> = {
    display: 'grid',
    gridAutoFlow: 'column',
    gridAutoColumns: '1fr',
    alignItems: 'start',
};

export const columnStyle: FelaStyle<any, any> = {
    padding: '16px',
    display: 'grid',
    rowGap: '16px',
    '> h4': {
        fontFamily: GRAPHIK,
        fontWeight: 400,
        fontSize: '18px',
        color: primary.eggplant,
        lineHeight: '32px',
        margin: 0,
    },
};
