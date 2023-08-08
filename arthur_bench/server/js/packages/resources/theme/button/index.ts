import secondary from '../../colors/Arthur/secondary';
import primary from '../../colors/Arthur/primary';
import { TRANSPARENT } from '../../style-constants';
import { EButtonVariation } from '../../../components/core/Button/typings';

export const primaryLightStyles = {
    backgroundColor: secondary.blue,
    disabledBackgroundColor: '#7FC0E6',
    progressBarBackgroundColor: '#70B8E3',
    focusBackgroundColor: '#2075A6',
    hoverBackgroundColor: '#2075A6',
    textColor: primary.white,
    disabledTextColor: '#CCE6F5',
    focusTextColor: primary.white,
    hoverTextColor: primary.white,
    linkColor: secondary.blue,
    linkFocusColor: '#2075A6',
    linkDisabledColor: '#A399A8',
    progressBarIndex: 0,
};

export const arthurLightStyles = {
    backgroundColor: primary.purple,
    disabledBackgroundColor: '#b099c8',
    progressBarBackgroundColor: '#b099c8',
    focusBackgroundColor: '#ac23f8',
    hoverBackgroundColor: '#ac23f8',
    textColor: primary.white,
    disabledTextColor: '#CCE6F5',
    focusTextColor: primary.white,
    hoverTextColor: primary.white,
    linkColor: primary.purple,
    linkFocusColor: '#ac23f8',
    linkDisabledColor: '#A399A8',
    progressBarIndex: 0,
};

export const secondaryLightStyles = {
    backgroundColor: TRANSPARENT,
    disabledBackgroundColor: TRANSPARENT,
    progressBarBackgroundColor: '#EAF5FB',
    focusBackgroundColor: TRANSPARENT,
    hoverBackgroundColor: TRANSPARENT,
    textColor: secondary.blue,
    disabledTextColor: '#7FC0E6',
    focusTextColor: '#2075A6',
    hoverTextColor: '#2688C2',
    linkColor: secondary.blue,
    linkFocusColor: '#2075A6',
    linkDisabledColor: '#A399A8',
    progressBarIndex: -1,
    borderColor: secondary.blue,
    hoverBorderColor: '#2688C2',
    focusBorderColor: '#2075A6',
    disabledBorderColor: '#7FC0E6',
};

export const arthurSecondaryLightStyles = {
    backgroundColor: TRANSPARENT,
    disabledBackgroundColor: TRANSPARENT,
    progressBarBackgroundColor: '#EAF5FB',
    focusBackgroundColor: TRANSPARENT,
    hoverBackgroundColor: TRANSPARENT,
    textColor: primary.purple,
    disabledTextColor: '#b099c8',
    focusTextColor: '#ac23f8',
    hoverTextColor: '#ac23f8',
    linkColor: primary.purple,
    linkFocusColor: '#ac23f8',
    linkDisabledColor: '#A399A8',
    progressBarIndex: -1,
    borderColor: primary.purple,
    hoverBorderColor: '#ac23f8',
    focusBorderColor: '#ac23f8',
    disabledBorderColor: '#b099c8',
};

export const subtleLightStyles = {
    backgroundColor: TRANSPARENT,
    disabledBackgroundColor: TRANSPARENT,
    progressBarBackgroundColor: '#F6F5F6',
    focusBackgroundColor: TRANSPARENT,
    hoverBackgroundColor: TRANSPARENT,
    textColor: '#473351',
    disabledTextColor: '#C8C2CB',
    focusTextColor: '#473351',
    hoverTextColor: '#473351',
    linkColor: '#473351',
    linkFocusColor: secondary.blue,
    linkDisabledColor: '#A399A8',
    borderColor: primary.ashGrey,
    hoverBorderColor: '#D1C9D1',
    focusBorderColor: '#AFA4AF',
    disabledBorderColor: '#EDEBED',
    progressBarIndex: -1,
};

export const destructiveLightStyles = {
    backgroundColor: secondary.red,
    disabledBackgroundColor: '#F28984',
    progressBarBackgroundColor: '#F07872',
    focusBackgroundColor: '#C34544',
    hoverBackgroundColor: '#DA4F4B',
    textColor: primary.white,
    disabledTextColor: '#FAD0CE',
    focusTextColor: primary.white,
    hoverTextColor: primary.white,
    linkColor: secondary.red,
    linkFocusColor: secondary.blue,
    linkDisabledColor: '#A399A8',
    progressBarIndex: 0,
};

export const buttonLightPalette = {
    [EButtonVariation.PRIMARY]: primaryLightStyles,
    [EButtonVariation.SECONDARY]: secondaryLightStyles,
    [EButtonVariation.SUBTLE]: subtleLightStyles,
    [EButtonVariation.DESTRUCTIVE]: destructiveLightStyles,
    [EButtonVariation.ARTHUR]: arthurLightStyles,
    [EButtonVariation.ARTHUR_SECONDARY]: arthurSecondaryLightStyles,
};

export const buttonDarkPalette = {
    [EButtonVariation.ARTHUR]: {
        ...arthurLightStyles,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.PRIMARY]: {
        ...primaryLightStyles,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.SECONDARY]: {
        ...secondaryLightStyles,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.SECONDARY]: {
        ...arthurSecondaryLightStyles,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.SUBTLE]: {
        ...subtleLightStyles,
        textColor: primary.ashGrey,
        hoverTextColor: '#CAC2CA',
        hoverBorderColor: '#CAC2CA',
        focusTextColor: '#AFA4AF',
        focusBorderColor: '#AFA4AF',
        borderColor: primary.ashGrey,
        disabledBorderColor: '#7F8087',
        disabledTextColor: '#7F8087',
        linkColor: primary.ashGrey,
        linkFocusColor: secondary.blue,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.DESTRUCTIVE]: {
        ...destructiveLightStyles,
        linkDisabledColor: '#7E7E86',
    },
};

export const buttonJPMCPalette = {
    [EButtonVariation.PRIMARY]: {
        ...primaryLightStyles,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.SECONDARY]: {
        ...secondaryLightStyles,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.SUBTLE]: {
        ...subtleLightStyles,
        textColor: primary.ashGrey,
        hoverTextColor: '#CAC2CA',
        hoverBorderColor: '#CAC2CA',
        focusTextColor: '#AFA4AF',
        focusBorderColor: '#AFA4AF',
        borderColor: primary.ashGrey,
        disabledBorderColor: '#7F8087',
        disabledTextColor: '#7F8087',
        linkColor: primary.ashGrey,
        linkFocusColor: secondary.blue,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.DESTRUCTIVE]: {
        ...destructiveLightStyles,
        linkDisabledColor: '#7E7E86',
    },
};

export const buttonJDPalette = {
    [EButtonVariation.PRIMARY]: {
        ...primaryLightStyles,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.SECONDARY]: {
        ...secondaryLightStyles,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.SUBTLE]: {
        ...subtleLightStyles,
        textColor: primary.ashGrey,
        hoverTextColor: '#CAC2CA',
        hoverBorderColor: '#CAC2CA',
        focusTextColor: '#AFA4AF',
        focusBorderColor: '#AFA4AF',
        borderColor: primary.ashGrey,
        disabledBorderColor: '#7F8087',
        disabledTextColor: '#7F8087',
        linkColor: primary.ashGrey,
        linkFocusColor: secondary.blue,
        linkDisabledColor: '#7E7E86',
    },
    [EButtonVariation.DESTRUCTIVE]: {
        ...destructiveLightStyles,
        linkDisabledColor: '#7E7E86',
    },
};
