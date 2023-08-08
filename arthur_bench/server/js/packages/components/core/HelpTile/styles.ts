import { FelaStyle } from 'react-fela';
import primary from 'resources/colors/Arthur/primary';
import { GRAPHIK } from 'resources/fonts';

const helpTopDiv = (notButton: boolean): FelaStyle<any, any> => ({
    width: '100%',
    height: '100%',
    boxSizing: 'border-box',
    backgroundColor: 'white',
    padding: '24px 32px',
    border: '1px solid #E4E0E4',
    borderRadius: '4px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    cursor: notButton ? 'default' : 'pointer',
    ':hover': {
        boxShadow: notButton ? 'none' : '0px 4px 12px rgba(26, 0, 22, 0.1)',
    },
});

const titleDiv: FelaStyle<any, any> = {
    display: 'flex',
    justifyContent: 'space-between',
    width: '100%',
};

const titleText = (disabled: boolean): FelaStyle<any, any> => ({
    fontFamily: GRAPHIK,
    fontSize: '24px',
    fontWeight: 400,
    lineHeight: '38.4px',
    color: disabled ? primary.ashGrey : primary.eggplant,
    letterSpacing: '-0.64px',
    margin: 0,
    display: 'flex',
    alignItems: 'center',
});

const subtitleText = (disabled: boolean): FelaStyle<any, any> => ({
    fontFamily: GRAPHIK,
    fontSize: '14px',
    fontWeight: 400,
    lineHeight: '160%',
    color: disabled ? primary.ashGrey : primary.eggplant,
});

const effortStyle = (disabled: boolean): FelaStyle<any, any> => ({
    display: 'flex',
    alignItems: 'flex-end',
    fontSize: '12px',
    color: disabled ? primary.ashGrey : primary.eggplant,
    opacity: 0.8,
});

export const helpTileStyle = {
    helpTopDiv,
    titleDiv,
    titleText,
    subtitleText,
    effortStyle,
};
