import primary from 'resources/colors/Arthur/primary';
import { MONO } from 'resources/fonts';

export const styles = {
    root: {
        display: 'flex',
        marginTop: '10px',
        alignItems: 'start',
        justifyContent: 'center',
        flexWrap: 'wrap',
        fontFamily: MONO,
        fontSize: '12px',
    },
    itemRoot: {
        display: 'flex',
        marginRight: '30px',
        ':last-child': {
            marginRight: 0,
        },
    },
    itemBase: (color: string) => ({
        display: 'inline-block',
        marginRight: '8px',
        backgroundColor: color,
        borderColor: color,
    }),
    itemHolder: {
        display: 'flex',
        flexDirection: 'column',
    },
    subtitle: {
        marginTop: '4px',
        color: primary.raisin,
        fontSize: '10px',
    },
    item: {
        line: {
            width: '12px',
            height: '2.5px',
            marginTop: '7px',
        },
        circle: {
            borderRadius: '10px',
            width: '7px',
            height: '7px',
            borderWidth: '3px',
            marginTop: '2px',
            borderStyle: 'solid',
            backgroundColor: 'transparent',
        },
        square: {
            width: '12px',
            height: '12px',
            marginTop: '2px',
        },
        dash: {
            width: '12px',
            height: '2.5px',
            marginLeft: '17px',
            marginRight: '25px',
            marginTop: '7px',
            position: 'relative',
            ':after': {
                content: '""',
                position: 'absolute',
                left: '-16px',
                display: 'inline-block',
                width: '12px',
                height: '2.5px',
                backgroundColor: 'inherit',
            },
            ':before': {
                content: '""',
                position: 'absolute',
                left: '16px',
                display: 'inline-block',
                width: '12px',
                height: '2.5px',
                backgroundColor: 'inherit',
            },
        },
    },
};
