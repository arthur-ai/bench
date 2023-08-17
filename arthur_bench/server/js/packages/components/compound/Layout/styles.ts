import primary from "resources/colors/Arthur/primary";
import secondary from "resources/colors/Arthur/secondary";
import { GRAPHIK_LIGHT } from "resources/fonts";

const styles = {
    body: {
        boxSizing: 'border-box',
        width: '100%',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: "space-between",
    },
    footer: {
        color: primary.eggplant,
        display: 'flex',
        justifyContent: 'flex-end',
        paddingTop: '20px',
        fontFamily: GRAPHIK_LIGHT,
        borderTop: "1px solid lightgrey",
        margin: '40px',
    },
    link: {
        color: secondary.blue,
    }
}

export default styles;
