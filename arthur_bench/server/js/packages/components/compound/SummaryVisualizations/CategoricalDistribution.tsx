import React from "react";
import BarChart from "../../core/Charts/BarChart";
import { ELegendItemShape } from "../../core/Charts/Legend/Legend";
import { chartColorsArray } from "resources/colors/Arthur/graphs";
import primary from "resources/colors/Arthur/primary";
import { useParams } from "react-router-dom";
import { TBarChartDataItem } from "../../core/Charts/BarChart/BarChart";
import { useFela } from "react-fela";
import styles from "./styles";
import { useTranslation } from "react-i18next";
import { CategoricalDistribution, TestRunSummary } from "../../../arthur-redux/slices/testSuites/types";

type TProps = {
    summaries: TestRunSummary[];
    total: number;
};

const getLegendItems = (summaries: TestRunSummary[], testRunId: string) => {
    return summaries.map((summary, i) => {
        const shape = summary.id === testRunId ? ELegendItemShape.DASH : ELegendItemShape.LINE;
        const color = summary.id === testRunId ? primary.black : chartColorsArray[i];

        return {
            color,
            name: summary.name,
            shape,
        };
    });
};

const formatGraphData = (inputData: TestRunSummary[], testRunId: string, total: number): TBarChartDataItem[] => {
    const transformedData: TBarChartDataItem[] = [];

    inputData.map((item, i) => {
        const entry: TBarChartDataItem = {
            color: item.id === testRunId ? primary.white : chartColorsArray[i],
            name: item.name,
            data: {},
            border: {
                color: item.id === testRunId ? primary.black : chartColorsArray[i],
                width: 1,
                type: item.id === testRunId ? "dashed" : "solid",
            },
        };

        item.histogram.map((histogramEntry) => {
            const { category, count } = histogramEntry as CategoricalDistribution;
            entry.data[category] = ((count / total) * 100).toFixed();
        });

        transformedData.push(entry);
    });

    return transformedData;
};

const formatTooltip = (event: { value: number; axisValueLabel: string; seriesName: string }[]) => {
    const label = `<div style='color: rgba(0, 0, 0, 0.6)'>${event[0]?.axisValueLabel}</div>`;
    const categories: string[] = event.map((item, i) => {
        return `<div>
                    <span style='background-color: ${chartColorsArray[i]}; width: 8px; height: 8px; display: inline-block; margin-right: 5px; border-radius: 8px'></span>
                    <div style='color: #000000'>${item.seriesName}: ${item.value}%</div>
                </div>`;
    });

    return label + categories.join("");
};

const CategoricalDistribution = (props: TProps) => {
    const { summaries, total } = props;
    const { css } = useFela();
    const { t } = useTranslation(["common"]);
    const params = useParams();
    const legendItems = getLegendItems(summaries, params.testRunId as string);
    const transformedData = formatGraphData(summaries, params.testRunId as string, total);

    return (
        <div className={css(styles.chartContainer)}>
            <div className={css(styles.title)}>{t("benchCharts.distribution")}</div>
            <div className={css(styles.subtitle)}>{t("benchCharts.distributionSubtitle")}</div>
            <BarChart
                graphData={transformedData}
                height={"300px"}
                legendItems={legendItems}
                showLegend
                useCustomLegendItems
                yAxisTitle={t("benchCharts.categoricalYAxis")}
                xAxisTitle={t("benchCharts.categoricalXAxis")}
                hideVerticalLines
                tooltip={formatTooltip}
            />
        </div>
    );
};

export default CategoricalDistribution;
