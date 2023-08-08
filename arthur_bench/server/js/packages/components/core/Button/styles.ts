import { getBorder, getPaddings } from './utils';
import { EButtonSize, EButtonVariation } from './typings';
import {
    ACTIVE,
    DISABLED,
    FOCUS,
    HOVER,
    NONE,
    UNDERLINE,
    TRANSPARENT,
} from 'resources/style-constants';
import { sizeParams } from './constants';
import { TThemeType } from 'resources/theme/types';
import { useFela } from 'react-fela';

const styles = (
    variation: EButtonVariation,
    size: EButtonSize,
    isLink: boolean,
    buttonTheme: TThemeType,
    iconStart: boolean,
    iconEnd: boolean,
    text: boolean,
    noBorder: boolean,
    customWidth?: string | number,
    customHeight?: string | number
) => {
    const colorPalette = buttonTheme.button[variation];
    const sizeParamValue = sizeParams[size];
    const { theme }: any = useFela();

    return {
        root: {
            ...(customWidth && { width: `${customWidth}px` }),
            ...(customHeight && { height: `${customHeight}px` }),
            ...(size === EButtonSize.FULL_WIDTH && { width: '100%' }),
            position: 'relative',
            display: 'inline-flex',
            whiteSpace: 'nowrap',
            alignItems: 'center',
            fontSize: `${sizeParamValue.text}px`,
            padding: getPaddings(size, iconStart, iconEnd, text),
            lineHeight: 1,
            ...(!noBorder && {
                boxShadow: getBorder(colorPalette.borderColor, isLink),
            }),
            border: NONE,
            cursor: 'pointer',
            fontFamily: theme.font_2,
            letterSpacing: '0.8px',
            textTransform: 'uppercase',
            backgroundColor: isLink
                ? TRANSPARENT
                : colorPalette.backgroundColor,
            color: isLink ? colorPalette.linkColor : colorPalette.textColor,
            '& path': {
                fill: isLink ? colorPalette.linkColor : colorPalette.textColor,
            },
            [HOVER]: {
                backgroundColor: isLink
                    ? TRANSPARENT
                    : colorPalette.hoverBackgroundColor,
                ...(!noBorder && {
                    boxShadow: getBorder(colorPalette.borderColor, isLink),
                }),
                color: isLink
                    ? colorPalette.linkColor
                    : colorPalette.hoverTextColor,
                '& path': {
                    fill: isLink
                        ? colorPalette.linkColor
                        : colorPalette.hoverTextColor,
                },
                textDecoration: isLink ? UNDERLINE : NONE,
            },
            [FOCUS]: {
                backgroundColor: isLink
                    ? TRANSPARENT
                    : colorPalette.focusBackgroundColor,
                ...(!noBorder && {
                    boxShadow: getBorder(colorPalette.borderColor, isLink),
                }),
                color: isLink
                    ? colorPalette.linkFocusColor
                    : colorPalette.focusTextColor,
                textDecoration: isLink ? UNDERLINE : NONE,
                '& path': {
                    fill: isLink
                        ? colorPalette.linkFocusColor
                        : colorPalette.focusTextColor,
                },
            },
            [ACTIVE]: {
                backgroundColor: isLink
                    ? TRANSPARENT
                    : colorPalette.backgroundColor,
                ...(!noBorder && {
                    boxShadow: getBorder(colorPalette.borderColor, isLink),
                }),
                color: isLink ? colorPalette.linkColor : colorPalette.textColor,
                '& path': {
                    fill: isLink
                        ? colorPalette.linkColor
                        : colorPalette.textColor,
                },
            },
            [DISABLED]: {
                pointerEvents: NONE,
                userSelect: NONE,
            },
        },
        disabled: {
            backgroundColor: isLink
                ? TRANSPARENT
                : colorPalette.disabledBackgroundColor,
            color: isLink
                ? colorPalette.linkDisabledColor
                : colorPalette.disabledTextColor,
            ...(!noBorder && {
                boxShadow: getBorder(colorPalette.borderColor, isLink),
            }),
            '& path': {
                fill: isLink
                    ? colorPalette.linkDisabledColor
                    : colorPalette.disabledTextColor,
            },
        },
        text: {
            width: '100%',
            position: 'relative',
            zIndex: 2,
            display: 'inline-block',
            marginLeft: iconStart ? `${sizeParamValue.iconTextMargin}px` : 0,
            marginRight: iconEnd ? `${sizeParamValue.iconTextMargin}px` : 0,
        },
        icon: {
            size: sizeParamValue.icon,
        },
        progressBar: {
            backgroundColor: colorPalette.progressBarBackgroundColor,
            position: 'absolute',
            zIndex: colorPalette.progressBarIndex,
            left: '0px',
            top: '0px',
            bottom: '0px',
        },
    };
};

export default styles;
