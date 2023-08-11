import { TSelectItem } from '@core/StyledSelect/StyledSelect';

export interface IMetricDropdownSelectionProps<T extends TSelectItem> {
    data: any[];
    onChange: (selectedItems: T[]) => void;
    selectedItems: T[];
    label?: string;
    handleApply?: any
}

export interface SelectedOptionProps {
    name: string;
    clickHandler: (name: string) => void;
}
