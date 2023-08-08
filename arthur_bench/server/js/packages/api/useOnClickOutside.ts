import React, { useEffect } from 'react';

type TOnClickOutsideHandler = (event: Event) => void;

const useOnClickOutside = (
    ref: React.RefObject<any>,
    handler: TOnClickOutsideHandler
) => {
    useEffect(() => {
        const listener: EventListener = (event: Event) => {
            if (!ref.current || ref.current.contains(event.target)) {
                return;
            }
            handler(event);
        };

        document.addEventListener('mousedown', listener);
        document.addEventListener('touchstart', listener);

        return () => {
            document.removeEventListener('mousedown', listener);
            document.removeEventListener('touchstart', listener);
        };
    }, [ref.current]);
};

export default useOnClickOutside;
