import { KeyboardEvent } from 'react';

/**
 *  Utility function that checks if the user pressed the enter key, then invokes
 *  a callback function if so.
 *
 *  Helps make the code A11Y compliant when non-interactive elements are used
 *  as handlers
 *
 * @param event Keyboard event (onKeyDown, onKeyUp, etc)
 * @param callback Function to call if the key was 'Enter'
 */
const checkIfEnter = (event: KeyboardEvent<HTMLDivElement>, callback: any) => {
    if (event.key === 'Enter') {
        callback();
    }
};

export default checkIfEnter;
