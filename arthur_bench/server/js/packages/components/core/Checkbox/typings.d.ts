import { FelaStyle } from 'react-fela';

export interface CheckboxProps {
    checked?: boolean;
    clickHandler?: (checked: boolean) => void;
    testId?: string;
    label?: string;
    checkboxStyle?: FelaStyle;
    iconStyle?: FelaStyle;
    labelStyle?: FelaStyle;
    styles?: any;
    color?: any;
    labelFontSize?: string;
    customDefaultColor?: string;
}
