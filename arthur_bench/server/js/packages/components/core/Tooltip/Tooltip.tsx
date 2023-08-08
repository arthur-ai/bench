import React, { useState } from 'react';
import { connect as connectStyles } from 'react-fela';
import { compose } from 'ui/helpers/compose';
import classnames from 'classnames';

import styles from './Tooltip.styles';

export type TTooltipPropsTypes = {
    width: number;
    delay: number;
    children: Element;
    styles: any;
    direction: string;
    content: any;
    styled?: boolean;
};

const Tooltip = (props: TTooltipPropsTypes) => {
    const { delay, children, styles, direction, content } = props;
    let timeout: any;
    const [active, setActive] = useState(false);

    const showTip = () => {
        timeout = setTimeout(() => {
            setActive(true);
        }, delay || 400);
    };

    const hideTip = () => {
        clearInterval(timeout);
        setTimeout(() => {
            setActive(false);
        }, 400);
    };

    return (
        <div
            className={styles.tooltipWrapper}
            onMouseEnter={showTip}
            onMouseLeave={hideTip}
        >
            <>
                {children}
                {active && (
                    <div
                        className={classnames(
                            styles.tooltipTip,
                            `styles.${direction}`
                        )}
                    >
                        {content}
                    </div>
                )}
            </>
        </div>
    );
};

export default compose(connectStyles(styles))(Tooltip);
