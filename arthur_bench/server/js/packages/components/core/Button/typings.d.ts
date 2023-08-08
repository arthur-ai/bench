import React, { ReactComponentElement } from 'react';

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    text: string | number;
    onClick: () => void;
    disabled?: boolean;
    className?: string;
    style?: Record<string, any>;
    testid?: string;
    ariarole?: string;
    icon?: ReactComponentElement;
    iconAlign?: 'left' | 'right';
}

export interface PrimaryButtonProps extends ButtonProps {
    color?: string;
}
