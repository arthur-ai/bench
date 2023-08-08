import { THEME_LIGHT, TThemeType } from './types';
import { buttonLightPalette as button } from './button';
import { tagSelectorPalette as tagSelector } from './tagSelector';
import primary from 'resources/colors/Arthur/primary';
import secondary from '../colors/Arthur/secondary';
import { GRAPHIK, MONO } from 'resources/fonts';

const themeLight: TThemeType = {
    name: THEME_LIGHT,
    bkg_1: secondary.variant.grey.active,
    bkg_2: primary.white,
    color_1: primary.purple,
    color_2: primary.white,
    color_3: primary.raisin,
    font_1: GRAPHIK,
    font_2: MONO,
    cta_color: secondary.blue,
    cta_color_hover: secondary.variant.blue.hover,
    cta_color_disabled: secondary.variant.blue.disabled,
    tagSelector,
    button,
};

export default themeLight;
