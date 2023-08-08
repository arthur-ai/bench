import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { MONO_MEDIUM } from 'resources/fonts';
import { TPosition } from './Dropdown';

const styles = ({ x, y }: TPosition) => {
    return {
        root: {
            zIndex: 101,
            position: 'absolute',
            left: `${x}px`,
            top: `${y}px`,
            filter: 'drop-shadow(0px 4px 8px rgba(26, 0, 22, 0.1))',
            background: primary.white,
        },
        header: {
            display: 'flex',
            justifyContent: 'space-between',
            padding: '12px 16px 12px 24px',
            background: primary.white,
        },
        title: {
            fontFamily: MONO_MEDIUM,
            fontSize: '12px',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: secondary.black,
        },
        closeIcon: {
            cursor: 'pointer',
        },
    };
};

export default styles;
