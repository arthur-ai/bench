import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { MONO } from 'resources/fonts';

const styles = {
    wrapper: {
        position: 'relative',
    },
    body: {
        height: 'auto',
        width: '225px',
        left: '0px',
        bottom: '-130px',
        padding: '14px 16px',
    },
    list: {
        padding: '0px',
        margin: '0px',
        listStyle: 'none',
        fontFamily: MONO,
        fontSize: '12px',
        lineHeight: '2',
    },
    option: {
        color: secondary.variant.grey.disabled,
        ':hover': {
            cursor: 'pointer',
            backgroundColor: secondary.lightBlue,
        },
        '& selected': {
            color: primary.eggplant,
            display: 'flex',
            justifyContent: 'space-between',
        },
    },
};

export default styles;
