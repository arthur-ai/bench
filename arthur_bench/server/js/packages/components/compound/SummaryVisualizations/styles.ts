import primary from "resources/colors/Arthur/primary";
import { MONO } from "resources/fonts";
import { ZRLineType } from "echarts/types/src/util/types";
import { chartColorsArray } from "resources/colors/Arthur/graphs";

const styles = {
    container: {
        display: "flex",
        gap: "30px",
        marginTop: "20px",
    },
    chartContainer: {
        backgroundColor: primary.white,
        color: primary.black,
        padding: "15px",
        width: "100%",
    },
    title: {
        fontSize: "18px",
    },
    subtitle: {
        fontFamily: MONO,
        fontSize: "12px",
        marginTop: "5px",
    },
    empty: {
        backgroundColor: primary.white,
        border: `0.5px dotted ${primary.ashGrey}`,
        padding: "50px",
        marginTop: "15px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    },
    tooltip: {
        display: "inline-block",
        marginRight: "8px",
        width: "8px",
        height: "8px",
        borderRadius: "8px",
        backgroundColor: "blue",
    },
};

export const baseItemStyle = (index: number) => ({
    color: chartColorsArray[index],
});

export const selectedItemStyle = {
    color: "#efefef",
    borderType: "dashed" as ZRLineType,
    borderColor: primary.black,
    borderWidth: 1,
    opacity: 0.8,
};

export default styles;
