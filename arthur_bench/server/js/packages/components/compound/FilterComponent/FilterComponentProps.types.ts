import { EIconType } from '../../core/Icon';

export type FilterComponentTypes =
    | 'square'
    | 'horizontal'
    | 'selection'
    | 'text';

export type FilterComponentProps = {
    icon?: EIconType;
    label: string;
    type: FilterComponentTypes;
    isActive?: boolean;
    clickHandler?: () => void;
    styles?: Record<any, any>;
    color?: string;
    bkgColor?: string;
};
