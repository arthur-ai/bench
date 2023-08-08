import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { GRAPHIK, MONO } from 'resources/fonts';

export const statusDropdownStyles = {
    backgroundColor: secondary.blue,
    color: primary.white,
    fontFamily: MONO,
    letterSpacing: '0.8px',
    fill: primary.white,
};
const styles = {
    container: {
        backgroundColor: 'white',
        height: '265px',
        width: '470px',
        margin: '18px',
        border: `1px solid ${primary.ashGrey}`,
        borderLeft: 'solid 5px #ffbf02',
        borderRadius: '2px',
        color: primary.eggplant,
    },
    box: {
        backgroundColor: '#f0f1f5',
        padding: '6px',
        fontFamily: MONO,
        display: 'inline-block',
        margin: '15px 0px',
        fontSize: '12px',
    },
    topRow: {
        display: 'flex',
        alignItems: 'flex-start',
        gap: '10px',
        margin: '0px 20px',
    },
    bottomRow: {
        display: 'flex',
        justifyContent: 'flex-end',
        margin: '20px',
        gap: '15px',
    },
    attributeLogic: {
        margin: '10px 20px',
        fontFamily: GRAPHIK,
        fontSize: '14px',
    },
    showAdditional: {
        margin: '0px 20px',
        fontSize: '14px',
        fontFamily: GRAPHIK,
        textDecoration: 'underline',
        ':hover': {
            color: secondary.blue,
        },
    },
};

export default styles;
