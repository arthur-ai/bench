import primary from "resources/colors/Arthur/primary";
import secondary from "resources/colors/Arthur/secondary";
import { MONO } from "resources/fonts";

const styles = {
    container: {
        background: primary.white,
        width: "968px",
        minHeight: "575px",
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        fontFamily: MONO,
        filter: "drop-shadow(0px 2px 12px rgba(26, 0, 22, 0.2))",
        color: primary.black,
    },
    header: {
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        padding: "32px",
    },
    body: {
        display: "flex",
        justifyContent: "space-evenly",
        minHeight: "427px",
        backgroundColor: secondary.variant.grey.active,
    },
    column: {
        display: "flex",
        flexDirection: "column",
        width: "435px",
        marginTop: "32px",
    },
    columnHeader: {
        background: primary.mint,
        height: "24px",
        display: "flex",
        justifyContent: "center",
        fontSize: "12px",
        alignItems: "center",
        marginBottom: "8px",
        borderRadius: "2px",
    },
    columnBody: {
        backgroundColor: primary.white,
        height: "300px",
        borderRadius: "2px",
        padding: "8px",
    },
    dataChunk: {
        fontSize: "14px",
        minHeight: "45px",
        padding: "7px",
        display: "flex",
        flexDirection: "column",
        overflowWrap: "anywhere",
        justifyContent: "space-between",
        margin: "8px 0",
        gap: "8px",
    },
    dataChunkLabel: {
        fontSize: "12px",
    },
    dataChunkBody: {
        overflow: "scroll",
        maxHeight: "110px",
    },
    title: {
        fontSize: "24px",
        fontWeight: 400,
        fontStyle: "normal",
        lineHeight: "38px",
        display: "flex",
        width: "100%",
    },
    tabs: {
        marginLeft: "32px",
    },
};

export default styles;
