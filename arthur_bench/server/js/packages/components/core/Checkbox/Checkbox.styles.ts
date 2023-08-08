import secondary from 'resources/colors/Arthur/secondary';
import { MONO } from 'resources/fonts';

const styles = {
    root: {
        display: 'flex',
        alignItems: 'center',
        overflow: 'hidden',
    },
    checkboxWrap: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
    },
    checkbox: (theme: any, color: string) => ({
        width: '18px',
        height: '18px',
        border: '2px solid #E4E0E4',
        appearance: 'none',
        display: 'inline-block',
        boxSizing: 'border-box',
        margin: 0,
        padding: 0,
        borderRadius: '2px',
        cursor: 'pointer',
        ':hover': {
            borderColor: color ? color : theme.color_1,
        },
        ':checked': {
            borderColor: color ? color : theme.color_1,
        },
    }),
    label: {
        cursor: 'pointer',
        marginLeft: '10px',
        fontSize: '14px',
        fontFamily: MONO,
        overflow: 'hidden',
        whiteSpace: 'nowrap',
        textOverflow: 'ellipsis',
    },
    icon: (theme: any, color: string) => ({
        display: 'block',
        transform: 'rotate(-45deg)',
        position: 'absolute',
        top: '4.5px',
        width: '8px',
        height: '4px',
        border: `2px solid ${color ? color : theme.color_1}`,
        borderRight: 'none',
        borderTop: 'none',
        pointerEvents: 'none',
    }),
};

export default styles;
