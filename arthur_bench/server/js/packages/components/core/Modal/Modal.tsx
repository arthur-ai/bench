import React, { ReactNode, useEffect, useRef } from 'react';
import defaultStyles from './styles';
import { useFela } from 'react-fela';

type Props = {
    children: ReactNode | string;
    styles?: any;
    showModal: boolean;
    setShowModal: (arg: boolean) => void;
};

const Modal = ({
    children,
    styles,
    showModal = false,
    setShowModal,
}: Props) => {
    if (!showModal) return null;
    const { css } = useFela();
    const baseStyle = defaultStyles().modalWrapper;
    const modalRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (
                modalRef.current &&
                modalRef.current.isEqualNode(event.target as Node)
            ) {
                showModal && setShowModal(false);
            }
        };
        if (modalRef.current) {
            modalRef.current.addEventListener('mousedown', handleClickOutside);
        }
        return () => {
            if (modalRef.current) {
                modalRef.current.removeEventListener(
                    'mousedown',
                    handleClickOutside
                );
            }
        };
    }, [modalRef, setShowModal]);

    return (
        <div ref={modalRef} className={css([baseStyle, styles])}>
            <div>{children}</div>
        </div>
    );
};

export default Modal;
