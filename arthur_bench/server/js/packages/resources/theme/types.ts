import { EButtonVariation } from '../../components/core/Button/typings';

export const THEME_DARK = 'dark';
export const THEME_LIGHT = 'light';

export type TThemeName = typeof THEME_DARK | typeof THEME_LIGHT;

export type TButtonPaletteType = {
    backgroundColor: string;
    disabledBackgroundColor: string;
    progressBarBackgroundColor: string;
    focusBackgroundColor: string;
    hoverBackgroundColor: string;
    textColor: string;
    disabledTextColor: string;
    focusTextColor: string;
    hoverTextColor: string;
    linkColor: string;
    linkFocusColor: string;
    linkDisabledColor: string;
    borderColor?: string;
    hoverBorderColor?: string;
    focusBorderColor?: string;
    disabledBorderColor?: string;
    progressBarIndex: number;
};

export type TTagSelectorPaletteType = {
    backgroundColor: string;
};

export type TThemeType = {
    name: TThemeName;
    bkg_1: string;
    bkg_2: string;
    color_1: string;
    color_2: string;
    color_3: string;
    font_1: string;
    font_2: string;
    cta_color: string;
    cta_color_hover: string;
    cta_color_disabled: string;
    tagSelector: TTagSelectorPaletteType;
    button: { [key in EButtonVariation]: TButtonPaletteType };
};
