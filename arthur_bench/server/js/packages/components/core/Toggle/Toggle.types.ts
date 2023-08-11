export type ToggleProps = {
    isActive: boolean;
    outlined?: boolean;
    disabled?: boolean;
    toggleIsActive?: (isActive: boolean) => void;
    width: number;
    height: number;
};
