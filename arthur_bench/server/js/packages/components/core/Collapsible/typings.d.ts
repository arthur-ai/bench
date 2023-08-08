import React, { FunctionComponent, HTMLAttributes } from 'react';

export interface CollapsibleProps extends HTMLAttributes<FunctionComponent> {
    testId?: string;
    open: boolean;
}
