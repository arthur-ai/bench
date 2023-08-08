import primary from 'resources/colors/Arthur/primary';

const activeStyles = {
    textDecoration: 'none !important',
    backgroundColor: 'white !important',
};

const styles = (isActive: boolean | undefined) => ({
    root: {
        color: `${primary.eggplant} !important`,
        borderRadius: '4px',
        transition: '0.5s',
        padding: '8px !important',
        ...(isActive && activeStyles),
        '&:hover': activeStyles,
        '& path': {
            transition: '0.5s',
            fill: `${primary.eggplant} !important`,
        },
    },
});

export default styles;
