import React, { useEffect, useState, useRef } from 'react';
import ReactDOM from 'react-dom';
import { useFela } from 'react-fela';
import styles from './styles';
import { TThemeType } from 'resources/theme/types';
import Icon, { EIconType } from '../Icon';
import primary from 'resources/colors/Arthur/primary';
import useOnClickOutside from "api/useOnClickOutside";

type TDropdownProps = {
    children: any;
    isOpen?: boolean;
    className?: string;
    handleClose: () => void;
    actionRef: React.RefObject<HTMLElement>;
    hasHeader?: boolean;
    preventClickOutside?: boolean;
    headerTitle?: string;
    alignRight?: boolean;
    inlineStyles?: Object;
};

export type TPosition = {
    x: number;
    y: number;
};

const Dropdown = (
    props: TDropdownProps
): React.ReactElement<TDropdownProps> | null => {
    const [position, setPosition] = useState<TPosition>({ x: 0, y: 0 });
    const { css } = useFela<TThemeType>();
    const {
        isOpen,
        children,
        actionRef,
        className = '',
        hasHeader,
        headerTitle,
        preventClickOutside,
        handleClose,
        alignRight
    } = props;

    const containerRef = useRef<HTMLDivElement>(null);

    useOnClickOutside(containerRef, () => {
        if (!preventClickOutside) {
            handleClose();
        }
    });

    const classNames = styles(position);

    const handleResizeEffect = () => {
        if (actionRef.current && containerRef.current) {
            const pos = actionRef.current.getBoundingClientRect();
            const y = pos.top + actionRef.current.offsetHeight + window.scrollY;
            const x = alignRight
                ? pos.left -
                  (containerRef.current?.offsetWidth -
                      actionRef.current.offsetWidth)
                : pos.left + window.scrollX;
            setPosition({ x, y });
        }
    };

    useEffect(() => handleResizeEffect(), [children]);

    useEffect(() => {
        window.addEventListener('resize', handleResizeEffect);
        return () => window.removeEventListener('resize', handleResizeEffect);
    }, []);

    const root = document.querySelector('#root');

    const renderContent = () => (
        <div
            style={props.inlineStyles}
            className={`${css(classNames.root)} ${className}`}
            ref={containerRef}
        >
            {hasHeader && (
                <div className={css(classNames.header)}>
                    {headerTitle && (
                        <div className={css(classNames.title)}>
                            {headerTitle}
                        </div>
                    )}
                    <div
                        role='presentation'
                        onClick={() => handleClose()}
                        className={css(classNames.closeIcon)}
                    >
                        <Icon
                            icon={EIconType.CANCEL}
                            size={20}
                            color={primary.raisin}
                        />
                    </div>
                </div>
            )}
            {children}
        </div>
    );

    if (!isOpen) return null;

    return ReactDOM.createPortal(renderContent(), root!);
};

export default Dropdown;
