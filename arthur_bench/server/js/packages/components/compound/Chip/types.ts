import { EIconType } from '../../core/Icon';
import { FelaStyle } from 'react-fela';

export enum EChipTheme {
    ARTHUR = 'arthur',
    DEFAULT = 'default',
    OUTLINED = 'outlined',
    PRODUCTION = 'production'
}

export type TChip = {
    id: string;
    name: string;
};

export type TChipProps = {
    onIconClick?: (tag: TChip) => void;
    chip?: TChip;
    chipName?: string | number;
    minimal?: boolean;
    iconStart?: EIconType;
    iconEnd?: EIconType;
    theme?: EChipTheme
    overrideStyles?: FelaStyle<{}>;
    iconStartColor?: string
};
