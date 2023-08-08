import React from 'react';
import { EIconType } from '../Icon';

export enum EButtonVariation {
    PRIMARY = 'primary',
    SECONDARY = 'secondary',
    SUBTLE = 'subtle',
    DESTRUCTIVE = 'destructive',
    ARTHUR = 'arthur',
    ARTHUR_SECONDARY = 'arthurSecondary',
}

export enum EButtonSize {
    LARGE = 'large',
    NORMAL = 'normal',
    SMALL = 'small',
    FULL_WIDTH = 'full_width',
}

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variation?: EButtonVariation;
    size?: EButtonSize;
    text?: string | number;
    isLink?: boolean;
    disabled?: boolean;
    className?: string;
    iconSize?: number;
    iconClass?: string;
    iconStart?: EIconType;
    iconText?: EIconType;
    iconEnd?: EIconType;
    isLoading?: boolean;
    loadingProgress?: number;
    style?: Record<string, any>;
    testId?: string;
    ariaRole?: string;
    clickHandler?: () => any;
    isHighlighted?: boolean;
    noBorder?: boolean;
    customWidth?: string | number;
    customHeight?: string | number;
}
