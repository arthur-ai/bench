import primary from 'resources/colors/Arthur/primary';
import { MONO } from 'resources/fonts';

const styles = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    color: primary.black,
    textTransform: 'uppercase',
    fontFamily: MONO,
    fontSize: '14px',
    margin: '10px 0px 20px 0px',
    '> p': {
        margin: '0px',
    },
};

export default styles;
