import primary from 'resources/colors/Arthur/primary';

const styles = {
    modal: {
        backgroundColor: primary.ashGrey,
        color: primary.black,
        display: 'flex',
    },
    imageContainer: {
        backgroundColor: primary.raisin,
        position: 'relative',
        height: '600px',
        '> img': {
            height: '100%',
        },
    },
    closeButton: {
        color: primary.white,
        position: 'absolute',
        top: '10px',
        right: '10px',
        cursor: 'pointer',
    },
    left: {
        width: '550px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        paddingTop: '15px',
    },
    helpTiles: {
        height: '200px',
        width: '450px',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        padding: '50px',
    },
    title: {
        display: 'flex',
        fontSize: '22px',
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
        '> img': {
            width: '200px',
            marginLeft: '-20px',
        },
    },
};

export default styles;
