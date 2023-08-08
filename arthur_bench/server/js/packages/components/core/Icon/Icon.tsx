import React from 'react';
import IcomoonReact from 'icomoon-react';
import { TIconProps } from './types';

const Icon = (props: TIconProps): React.ReactElement<TIconProps> => {
    const {
        color,
        size,
        icon,
        className = '',
        style,
        clickHandler,
        testId = 'arthurIcon',
    } = props;
    const { iconSet } = window;
    return (
        <div
            style={{
                display: 'inline-block',
                cursor: clickHandler && 'pointer',
            }}
            role={clickHandler ? 'button' : 'figure'}
            onKeyDown={() => {}}
            onClick={clickHandler}
            data-testid={testId}
        >
            <IcomoonReact
                style={style}
                className={className}
                iconSet={iconSet}
                color={color}
                size={size}
                icon={icon}
            />
        </div>
    );
};

export default Icon;
