import { EButtonSize } from './typings';

export const getProgressBarWidth = (progress: number): number => {
    if (progress < 0) {
        return 0;
    } else if (progress > 100) {
        return 100;
    } else {
        return progress;
    }
};

export const getBorder = (color: string | undefined, isLink: boolean) =>
    color && !isLink ? `0px 0px 0px 2px ${color} inset` : 'none';

export const getPaddings = (
    size: EButtonSize,
    iconStart: boolean,
    iconEnd: boolean,
    text: boolean
): string => {
    const anyIconApplied = iconEnd || iconStart;
    const isSingleIcon =
        ((!iconEnd && iconStart) || (iconEnd && !iconStart)) && !text;

    if (isSingleIcon) {
        switch (size) {
            case EButtonSize.LARGE:
                return '14.5px 18.5px';
            default:
                return '10px';
        }
    } else {
        switch (size) {
            case EButtonSize.SMALL:
                return `${anyIconApplied ? 9 : 10}px ${iconEnd ? 8 : 16}px ${
                    anyIconApplied ? 9 : 10
                }px ${iconStart ? 8 : 16}px`;
            case EButtonSize.LARGE:
                return `${anyIconApplied ? 14.5 : 19}px ${
                    iconEnd ? 19 : 24
                }px ${anyIconApplied ? 14.5 : 19}px ${iconStart ? 19 : 24}px`;
            default:
                return `${anyIconApplied ? 10 : 13}px ${iconEnd ? 9.5 : 16}px ${
                    anyIconApplied ? 10 : 13
                }px ${iconStart ? 9.5 : 16}px`;
        }
    }
};
