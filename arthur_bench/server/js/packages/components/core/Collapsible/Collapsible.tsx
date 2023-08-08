import React, { useEffect, useRef, useState } from 'react';
import { useFela } from 'react-fela';

import { CollapsibleProps } from './typings';
import { defaultStyle } from './styles';

type TCollapsibleContext = {
    updateSize: (() => void) | null;
};

export const CollapsibleContext = React.createContext<TCollapsibleContext>({
    updateSize: null,
});

function Collapsible(props: CollapsibleProps) {
    const { css } = useFela();
    const [height, setHeight] = useState<number | undefined>(0);
    const contentRef = useRef<HTMLDivElement>(null);
    const { open, testId = 'collapsible-toggle' } = props;

    const combinedStyle = {
        ...defaultStyle(open),
        ...(props.style ? props.style : {}),
    };

    useEffect(() => {
        if (open) {
            setHeight(contentRef?.current?.scrollHeight);
        } else {
            setHeight(0);
        }
    }, [open, props.children]);

    const updateSize = () => {
        setTimeout(() => {
            setHeight(
                (contentRef?.current?.firstChild as HTMLElement)?.scrollHeight
            );
        }, 100);
    };

    return (
        <div
            className={`${props.className || ''} ${css(combinedStyle)}`}
            ref={contentRef}
            style={{ height: open ? '100%' : height }}
            data-testid={testId}
        >
            <CollapsibleContext.Provider value={{ updateSize }}>
                {props.children}
            </CollapsibleContext.Provider>
        </div>
    );
}

export default Collapsible;
