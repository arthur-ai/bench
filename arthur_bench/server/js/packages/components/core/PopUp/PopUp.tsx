import React, { LegacyRef, ReactNode, Ref, useEffect, useRef, useState } from 'react';
import defaultStyles from './styles';
import { useFela } from 'react-fela';
import Icon, { EIconType } from '../Icon';
import useOnClickOutside from "api/useOnClickOutside";

type Props = {
    children: ReactNode | string;
    styles?: any;
    showPopUp: boolean;
    customMinHeight?: number
    noScroll?: boolean;
    anchorRef?: any;
    alignRight?: boolean;
    alignTop?: boolean;
    hasCloseOption?: boolean;
    preventCloseOnOutsideClick?: boolean;
    closeHandler?: () => void;
    setShowPopUp: (arg: boolean) => void;

};

const TOP_ALIGN_PADDING = 30

const PopUp = (props: Props) => {
    const {
        children,
        styles,
        showPopUp = false,
        customMinHeight,
        noScroll = true,
        anchorRef = null,
        alignRight = false,
        alignTop = false,
        hasCloseOption = false,
        preventCloseOnOutsideClick,
        closeHandler,
        setShowPopUp,
    } = props;
    const { css } = useFela();
    const baseStyle = defaultStyles(customMinHeight).popUpWrapper;
    const [ refStyles, setRefStyles ] = useState({})
    const containerRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        document.body.style.overflow = showPopUp && noScroll ? 'hidden' : 'unset';
    }, [showPopUp]);


    useOnClickOutside(containerRef, () => {
        if (!preventCloseOnOutsideClick) {
            setShowPopUp(false);
        }
    });

    const handleResizeEffect = () => {
        if (anchorRef && anchorRef.current && containerRef && containerRef.current) {
            const pos = anchorRef.current.getBoundingClientRect();
            const top = alignTop ? pos.top + window.scrollY + TOP_ALIGN_PADDING : pos.top + anchorRef.current.offsetHeight + window.scrollY;
            const left = alignRight
            ? pos.left -
              (containerRef.current?.offsetWidth -
                anchorRef.current.offsetWidth)
            : pos.left + window.scrollX;
            setRefStyles({ top: `${top}px`, left: `${left}px` });
        }
    };

    useEffect(() => handleResizeEffect(), [children, showPopUp]);

    if (showPopUp) {
        return (
            <div ref={containerRef} className={css([baseStyle, styles, refStyles])}>{children}
                {hasCloseOption && closeHandler && <Icon className={css(defaultStyles(customMinHeight).popUpCloseButton)} icon={EIconType.CLOSE_CIRCLE} size={12} clickHandler={closeHandler}/>}
            </div>);
    }

    return null;
};

export default PopUp;
