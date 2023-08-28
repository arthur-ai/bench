import primary from "resources/colors/Arthur/primary";
import secondary from "resources/colors/Arthur/secondary";
import {GRAPHIK, GRAPHIK_LIGHT, MONO} from "resources/fonts";

const styles = {
    container: {
        backgroundColor: primary.white,
        width: '90%',
        border: `1px solid ${primary.ashGrey}`,
        marginBottom: '20px',
        color: primary.black,
        fontFamily: MONO,
        padding: '10px 20px',
        fontSize: '14px'
    },
    date: {
        textAlign: 'right',
    },
    name: {
        color: secondary.blue,
        fontFamily: GRAPHIK_LIGHT,
        fontSize: '18px',
        ':hover': {
            cursor: 'pointer',
            textDecoration: 'underline'
        }
    },
    row: {
        display: 'grid',
        gridTemplateColumns: '1fr 150px 1fr',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        margin: '10px',
        textAlign: 'left',
        padding: '10px'
    },
    hr: {
        border:`1px solid ${primary.ashGrey}`,
        margin: '15px 0px'
    },
    tag: (color: string) => ({
        border: `2px solid ${color}`,
        borderRadius: '5px',
        padding: '5px',
        width: 'fit-content',
    })
};

export default styles;
