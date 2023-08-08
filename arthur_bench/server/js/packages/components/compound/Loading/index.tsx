import React from 'react';
import { useFela } from 'react-fela';
import renderer from '../../../../src/renderer';
import icon from 'resources/images/Arthur_Logo_Symbol_low_margin.svg';

const loadingkeyframe = () => ({
    '0%': {
        transform: 'rotate(0deg)',
    },
    '100%': {
        transform: 'rotate(360deg)',
    },
});

const loadingAnimation = renderer.renderKeyframe(loadingkeyframe, {});

const Loading = ({ isCentered = true }: { isCentered?: boolean }) => {
    const { css } = useFela();
    return (
        <img
            alt='loading'
            className={css({
                animationName: loadingAnimation,
                animationIterationCount: 'infinite',
                animationDuration: '0.5s',
                marginTop: '15px',
                ...(isCentered
                    ? { position: 'absolute', left: '50%', top: '50%' }
                    : {}),
            })}
            src={icon}
        />
    );
};

export default Loading;
