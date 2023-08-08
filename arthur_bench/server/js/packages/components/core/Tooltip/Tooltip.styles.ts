import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { GRAPHIK } from 'resources/fonts';
import { TTooltipPropsTypes } from './Tooltip';

const styles = ({ direction, styled, width }: TTooltipPropsTypes) => ({
    tooltipWrapper: {
        display: 'inline-block',
        position: 'relative',
        cursor: 'pointer',
    },
    tooltipTip: {
        position: 'absolute',
        borderRadius: styled ? '4px' : '2px',
        left: '50%',
        transform: 'translateX(-50%)',
        padding: styled ? '4px 8px' : '16px',
        color: primary.eggplant,
        background: styled ? secondary.variant.grey.active : primary.white,
        textAlign: 'left',
        ...(styled
            ? {
                  width: `${width}px` || '320px',
                  fontSize: '14px',
                  ':after': {
                      content: '""',
                      position: 'absolute',
                      width: 0,
                      height: 0,
                      left: 0,
                      right: 0,
                      bottom: '-6px',
                      borderStyle: 'solid',
                      margin: 'auto',
                      borderWidth: '8px 6px 0 6px',
                      borderColor: `${secondary.variant.grey.active} transparent transparent transparent`,
                  },
              }
            : {
                  width: width ? `${width}px` : '320px',
                  minHeight: '50px',
                  fontSize: '12px',
              }),
        boxShadow: 'rgb(26 0 22 / 16%) 0px 6px 8px',
        fontWeight: 400,
        fontFamily: GRAPHIK,
        lineHeight: '2',
        zIndex: '100',
        whiteSpace: 'wrap',
        ...(direction === 'top' && {
            top: 'calc(-60px)',
            '::before': {
                top: '100%',
            },
        }),
        ...(direction === 'right' && {
            left: 'calc(100% + 10px)',
            right: 'auto',
            top: '50%',
            transform: 'translateX(0) translateY(-50%)',
            '::before': {
                left: 'calc(6 * -1)',
                top: '50%',
                transform: 'translateX(0) translateY(-50%)',
                borderRightColor: 'black',
            },
        }),
        ...(direction === 'bottom' && {
            '::before': {
                bottom: '100%',
                borderBottomColor: 'black',
            },
        }),
        ...(direction === 'left' && {
            left: 'auto',
            right: 'calc(100% + 10px)',
            top: '50%',
            transform: 'translateX(0) translateY(-50%)',
            '::before': {
                left: 'auto',
                right: 'calc(6 * -2)',
                top: '50%',
                transform: 'translateX(0) translateY(-50%)',
                borderLeftColor: 'black',
            },
        }),
        '::before': {
            content: ' ',
            left: '50%',
            border: 'solid transparent',
            height: '0',
            width: '0',
            position: 'absolute',
            pointerEvents: 'none',
            borderWidth: '6px',
            marginLeft: 'calc(6 * -1)',
        },
    },
});

export default styles;
