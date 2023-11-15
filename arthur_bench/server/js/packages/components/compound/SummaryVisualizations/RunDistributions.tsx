import React from "react";
import LineChart from "../../core/Charts/LineChart";
import { Distribution, TestRunSummary, Histogram } from "../../../arthur-redux/slices/testSuites/types";
import { TGraphDataItem } from "../../core/Charts/LineChart/";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";

const getValues = (summaries: TestRunSummary[], testRunId: string, total: number): TGraphDataItem[] => {
    return summaries.map((summary: TestRunSummary) => {
        const formattedData: Array<[number, number] | [number]> = summary.histogram.map((t: Histogram) => {
            const { low } = t as Distribution;

            return [parseFloat(low.toFixed(3)), (t.count / total) * 100];
        });

        return {
            name: summary.name,
            data: formattedData,
            isReference: summary.id === testRunId,
        };
    });
};

type Props = {
    summaries: TestRunSummary[];
    total: number;
};
const RunDistributions = ({ summaries, total }: Props) => {
    const { t } = useTranslation(["common"]);
    const params = useParams();
    const values = getValues(summaries, params.testRunId as string, total);

    return (
        <LineChart
            id={params.testSuiteId}
            graphData={values}
            showLegend
            height={"300px"}
            yAxisTitle={t("visualization.distributionYAxis")}
            xAxisTitle={t("visualization.distributionXAxis")}
            smoothData
            hasDefaultTooltip={true}
        />
    );
};

export default RunDistributions;
