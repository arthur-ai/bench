import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';

const styles = ({ theme, type, isActive, color, bkgColor }: any) => ({
    wrap: {
        overflow: 'hidden',
        display:
            type === 'horizontal' || type === 'selection' || type === 'square'
                ? 'flex'
                : 'block',
        alignItems: 'center',
        ...(color && isActive && { border: `1px solid ${color}` }),
        ...(!color &&
            isActive && {
                border: `1px solid ${
                    isActive ? secondary.blue : primary.ashGrey
                }`,
            }),
        borderRadius: '4px',
        cursor: 'pointer',
        padding:
            type === 'selection' || type === 'text' ? '4px 5px' : '10px 15px',
        ...(type === 'square' && {
            textAlign: 'center',
            width: '80px',
            height: '80px',
            flexDirection: 'column',
            justifyContent: 'center',
            padding: 0,
        }),
        ...(isActive && {
            background: bkgColor ? bkgColor : secondary.lightBlue,
        }),

        ':hover': {
            background: bkgColor ? bkgColor : secondary.lightBlue,
        },
    },
    icon: {
        ...(type === 'square' && {
            marginBottom: '10px',
        }),
        fill: color ? color : secondary.blue,
    },
    label: {
        marginLeft:
            type === 'square' ? '0' : type === 'selection' ? '5px' : '12px',
    },
});

export default styles;
