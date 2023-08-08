import primary from 'resources/colors/Arthur/primary';
import { MONO } from 'resources/fonts';

const styles = {
    container: {
        display: 'flex',
        gap: '30px',
        marginTop: '20px',
    },
    chartContainer: {
        backgroundColor: primary.white,
        color: primary.black,
        padding: '15px',
        width: '50%',
        border: `0.5px solid ${primary.ashGrey}`,
    },
    title: {
        fontSize: '18px',
    },
    subtitle: {
        fontFamily: MONO,
        fontSize: '12px',
        marginTop: '5px',
    },
    empty: {
        backgroundColor: primary.white,
        border: `0.5px dotted ${primary.ashGrey}`,
        padding: '50px',
        marginTop: '15px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
    },
};

export default styles;
