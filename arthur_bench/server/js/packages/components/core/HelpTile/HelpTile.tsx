import React, { useState } from 'react';
import { useFela } from 'react-fela';

import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import Icon from '../Icon';
import checkIfEnter from 'utils/keypress-enter';

import { HelpTileProps } from './typings';
import { helpTileStyle } from './styles';

function HelpTile(props: HelpTileProps) {
    const { css } = useFela();
    const [iconColor, setColor] = useState(primary.ashGrey);
    const { disabled = false } = props;

    const mouseOver = () => {
        if (!disabled) {
            setColor(secondary.blue);
        }
    };

    const mouseLeave = () => {
        setColor(primary.ashGrey);
    };

    const clickHandler = () => {
        if (props.link && !disabled) {
            window.open(props.link);
        }
    };

    const handleKeypress = (e: any) => {
        checkIfEnter(e, clickHandler);
    };

    const notButton = !props.link || disabled;

    return (
        <div
            className={css(helpTileStyle.helpTopDiv(notButton))}
            onMouseOver={mouseOver}
            onFocus={mouseOver}
            onMouseLeave={mouseLeave}
            onBlur={mouseLeave}
            tabIndex={disabled ? -1 : 0}
            onClick={clickHandler}
            onKeyDown={handleKeypress}
            role='button'
        >
            <div className={css(helpTileStyle.titleDiv)}>
                <div>
                    <h3 className={css(helpTileStyle.titleText(disabled))}>
                        {props.titleIcon ? props.titleIcon : null}
                        {props.title}
                    </h3>
                    <p className={css(helpTileStyle.subtitleText(disabled))}>
                        {props.description}
                    </p>
                </div>
                {props.icon ? (
                    <Icon icon={props.icon} size={30} color={iconColor} />
                ) : null}
            </div>
            {props.effort ? (
                <div className={css(helpTileStyle.effortStyle(disabled))}>
                    {props.effort}
                </div>
            ) : null}
        </div>
    );
}

export default HelpTile;
