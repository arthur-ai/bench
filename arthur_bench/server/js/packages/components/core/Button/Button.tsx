import React, { ForwardedRef } from 'react';
import { useFela } from 'react-fela';
import { ButtonProps, EButtonSize, EButtonVariation } from './typings';
import styles from './styles';
import Icon from '../Icon/Icon';
import { isNil } from 'utils/is-nil';
import { getProgressBarWidth } from './utils';
import { TThemeType } from 'resources/theme/types';

const Button = React.forwardRef(
    (props: ButtonProps, ref: ForwardedRef<HTMLButtonElement>) => {
        const { css, theme } = useFela<TThemeType>();

        const {
            variation = EButtonVariation.PRIMARY,
            size = EButtonSize.NORMAL,
            iconStart,
            iconEnd,
            iconText,
            isLoading,
            loadingProgress = 0,
            iconSize,
            iconClass,
            isLink = false,
            text,
            disabled,
            style,
            clickHandler,
            noBorder = false,
            customWidth = 0,
            customHeight = 0,
        } = props;

        const classNames = styles(
            variation,
            size,
            isLink,
            theme,
            !!iconStart,
            !!iconEnd,
            !isNil(text),
            noBorder,
            customWidth,
            customHeight
        );

        const renderProgressBar = () => {
            if (isLoading && !isLink) {
                return (
                    <div
                        className={css(classNames.progressBar, {
                            width: `${getProgressBarWidth(loadingProgress)}%`,
                        })}
                    />
                );
            }

            return null;
        };

        return (
            <button
                ref={ref}
                style={style}
                data-testid={props.testId}
                aria-roledescription={props.ariaRole}
                disabled={disabled || isLoading}
                className={`${css(
                    { ...props.style },
                    classNames.root,
                    disabled ? classNames.disabled : {}
                )} ${props.className} `}
                onClick={clickHandler ? clickHandler : () => {}}
            >
                {renderProgressBar()}
                {iconStart && (
                    <Icon
                        className={iconClass}
                        size={iconSize || classNames.icon.size}
                        icon={iconStart}
                    />
                )}
                {text && (
                    <span className={css(classNames.text)}>
                        {
                            <div>
                                {iconText && (
                                    <Icon
                                        className={iconClass}
                                        size={iconSize || classNames.icon.size}
                                        icon={iconText}
                                    />
                                )}
                                {text}
                            </div>
                        }
                    </span>
                )}
                {props.children ? props.children : null}
                {iconEnd && (
                    <Icon
                        className={iconClass}
                        size={iconSize || classNames.icon.size}
                        icon={iconEnd}
                    />
                )}
            </button>
        );
    }
);

Button.displayName = 'ArthurButton';

export default Button;
