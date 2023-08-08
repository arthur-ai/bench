import { ReactNode } from 'react';
import { FelaStyle } from 'react-fela';
import { EIconType } from '../Icon';

export interface HelpTileProps {
    title: string;
    titleIcon?: ReactNode;
    description: string | ReactNode;
    link?: string;
    icon?: EIconType;
    effort?: string;
    disabled?: boolean;
}
