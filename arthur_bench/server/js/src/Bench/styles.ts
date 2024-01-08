import primary from "resources/colors/Arthur/primary";
import { GRAPHIK_LIGHT } from "resources/fonts";

const styles = {
    container: {
        padding: "0px 50px 40px 50px",
        color: primary.black,
    },
    banner: {
        backgroundColor: primary.white,
        color: primary.black,
        padding: "15px 30px",
        fontFamily: GRAPHIK_LIGHT,
        display: "flex",
        gap: "20px",
    },
    header: {
        boxSizing: "border-box",
        width: "100%",
        background: primary.white,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        color: primary.black,
        padding: "24px 24px 0 24px",
    },
    topRow: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: "20px",
    },
    bottomRow: {
        backgroundColor: primary.white,
        padding: "20px",
        color: primary.black,
        fontSize: "20px",
    },
    middleRow: {
        padding: "20px",
        color: primary.black,
        fontSize: "20px",
    },
    inputOutput: {
        backgroundColor: primary.white,
        margin: "20px",
        padding: "20px",
        color: primary.black,
        width: "fit-content",
    },
    drawer: {
        padding: "20px",
        color: primary.black,
        border: `1px ${primary.ashGrey}`,
        borderStyle: "solid none",
        display: "flex",
        justifyContent: "flex-start",
        flexDirection: "column",
        gap: "15px",
        transitionDuration: "0.5s",
    },
    tableContainer: {
        backgroundColor: primary.white,
        padding: "30px 20px",
        overflow: "scroll",
    },
    emptyState: {
        backgroundColor: primary.white,
        height: "360px",
        width: "680px",
        border: `1px dashed ${primary.ashGrey}`,
        color: primary.black,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: "25px",
    },
    compareContainer: {
        display: "flex",
        flexDirection: "column",
        gap: "20px",
        margin: "20px",
    },
};

export default styles;
