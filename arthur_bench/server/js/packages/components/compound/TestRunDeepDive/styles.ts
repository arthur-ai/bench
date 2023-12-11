import primary from "resources/colors/Arthur/primary";
import secondary from "resources/colors/Arthur/secondary";
import { GRAPHIK_LIGHT, MONO, MONO_MEDIUM } from "resources/fonts";
import hexToRgba from "../../../utils/hex-to-rgba/hex-to-rgba"
import { GRAPHIK } from "resources/fonts/";

const styles = {
    headerCell: (color: string) => ({
        backgroundColor: color,
        fontFamily: MONO_MEDIUM,
        border: `1px solid ${primary.ashGrey}`,
        borderBottom: `1px solid ${secondary.darkGrey}`,
        textAlign: "left",
    }),
    table: {
        borderCollapse: "collapse",
        border: `1px solid ${primary.ashGrey}`,
        overflow: "scroll",
    },
    cell: (width?: string) => ({
        border: `1px solid ${primary.ashGrey}`,
        fontSize: "16px",
        FontFamily: GRAPHIK_LIGHT,
        textAlign: "left",
        padding: "16px",
        width: width ?? "auto",
    }),
    body: {
        backgroundColor: primary.white,
        padding: "16px",
        overflow: "scroll",
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
    },
    score: (color: string) => ({
        backgroundColor: color,
        color: primary.white,
        padding: "4px 8px",
        borderRadius: "4px",
        display: "inline-block",
        margin: "0 12px",
    }),
    container: {
        background: primary.white,
        width: "968px",
        maxHeight: "575px",
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
        padding: "16px",
        borderBottom: `1px solid ${primary.ashGrey}`,
        fontFamily: MONO,
        fontSize: "12px",
        alignItems: "center",
    },
    content: {
        display: "flex",
        flexDirection: "column",
        gap: "16px",
    },
    textBox: {
        display: "flex",
        flexDirection: "column",
        maxHeight: "250px",
        maxWidth: "450px",
        minWidth: "450px",
        border: `1px solid ${primary.ashGrey}`,
        borderRadius: "4px",
    },
    textBoxHeader: (color: string) => ({
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        backgroundColor: hexToRgba(color, 0.4),
        borderBottom: `1px solid ${secondary.darkGrey}`,
        padding: "8px",
        fontFamily: MONO,
        fontSize: "12px",
    }),
    textBoxBody: {
        overflow: "scroll",
        padding: "8px",
        fontFamily: GRAPHIK,
        fontSize: "14px",
    },
    headerText: {
        fontFamily: GRAPHIK,
        fontSize: "18px",
    },
    expandableTableCell: {
        maxWidth: "450px",
        minWidth: "300px",
        textAlign: "left" as const,
        border: `1px solid ${primary.ashGrey}`,
        padding: "12px",
        overflow: "auto" as const,
        fontSize: "16px",
    },
    tableBody: {
        overflow: "scroll",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        backgroundColor: primary.white,
        padding: "16px",
    },
};

export default styles;
