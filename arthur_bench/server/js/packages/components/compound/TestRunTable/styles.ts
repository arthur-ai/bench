import primary from "resources/colors/Arthur/primary";
import secondary from "resources/colors/Arthur/secondary";
import { GRAPHIK_LIGHT, MONO } from "resources/fonts";
import { GRAPHIK } from "resources/fonts/";

const styles = {
    table: {
        borderCollapse: "collapse",
        border: `1px solid ${primary.ashGrey}`,
        margin: "20px",
    },
    runName: {
        display: "flex",
        flexDirection: "column",
        gap: "10px",
    },
    row: (checked: boolean) => ({
        height: "60px",
        backgroundColor: checked ? secondary.lightBlue : primary.white,
        ":hover": {
            backgroundColor: secondary.lightBlue,
        },
    }),
    nameCell: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
    },
    empty: {
        backgroundColor: primary.white,
        height: "360px",
        width: "680px",
        border: `1px dashed ${primary.ashGrey}`,
        color: primary.black,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: "30px",
    },
    tableContainer: {
        display: "flex",
        flexDirection: "column",
    },
    container: {
        display: "flex",
        flexDirection: "row-reverse",
        alignItems: "start",
        justifyContent: "space-between",
    },
    button: {
        display: "flex",
        gap: "10px",
        alignItems: "center",
        fontFamily: GRAPHIK,
        color: secondary.variant.grey.disabled,
        fontSize: "12px",
    },
};

export const cellStyles = (width?: string) => ({
    width: width ?? "auto",
    border: `1px solid ${primary.ashGrey}`,
    fontSize: "14px",
    FontFamily: GRAPHIK_LIGHT,
    textAlign: "left",
    padding: "16px",
});

export const headerCell = (color?: string) => ({
    backgroundColor: color ?? primary.white,
    fontFamily: MONO,
    border: `1px solid ${primary.ashGrey}`,
    textAlign: "left",
    fontSize: "16px",
});

export default styles;
