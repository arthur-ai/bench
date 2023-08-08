import primary from 'resources/colors/Arthur/primary';

const styles = (customMinHeight?: number) => ({
    popUpWrapper: {
        background: primary.white,
        position: 'absolute',
        left: '15px',
        bottom: '75px',
        padding: '15px 25px',
        width: '225px',
        minHeight: customMinHeight ? `${customMinHeight}px` : '425px',
        filter: 'drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25))',
        borderRadius: '2px',
        zIndex: '2'
    },
    popUpCloseButton: {
        position: 'absolute',
        top: '10px',
        right: '10px'
    }
});

export default styles;
