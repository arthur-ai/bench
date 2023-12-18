import React from 'react';
import BarChart from '../../core/Charts/BarChart';
import {useFela} from 'react-fela';
import {TestRunSummary} from "../../../arthur-redux/slices/testSuites/types"
import {ZRLineType} from "echarts/types/src/util/types";
import {useParams} from "react-router-dom";
import {ELegendItemShape} from "../../core/Charts/Legend/Legend";
import { chartColorsArray } from 'resources/colors/Arthur/graphs';
import primary from 'resources/colors/Arthur/primary';

const baseItemStyle = (index: number) => ({
    color: chartColorsArray[index],
});

const selectedItemStyle = {
    color: '#efefef',
    borderType: 'dashed' as ZRLineType,
    borderColor: primary.black,
    borderWidth: 1,
    opacity: 0.8,
};


const getValues = (summaries: TestRunSummary[], testRunId: string) => {
    return summaries.map((summary: TestRunSummary, i) => {
        let itemStyle = summary.id === testRunId ? selectedItemStyle : baseItemStyle(i);
        return {
            itemStyle,
            value: summary.avg_score,
            name: summary.name,
        }
    });
};

const getLegendItems = (summaries: TestRunSummary[], testRunId: string) => {
    return summaries.map((summary, i) => {
        let shape = summary.id === testRunId ? ELegendItemShape.DASH : ELegendItemShape.LINE;
        let color = summary.id === testRunId ? primary.black : chartColorsArray[i];
        return {
            color,
            name: summary.name,
            shape,
        }});
}

type Props = {
    summaries: TestRunSummary[];
};
const AverageScores = ({ summaries }: Props) => {
    const params = useParams();
    const { css } = useFela();
    const values = getValues(summaries, params.testRunId as string);
    const legendItems = getLegendItems(summaries, params.testRunId as string);

    return (
        <div>
            <BarChart
                options={{
                    xAxis: { type: 'value' },
                    yAxis: { type: 'category', data: [] },
                    series: [
                        {
                            type: 'bar',
                            data: values,
                        },
                    ],
                }}
                barWidth={'20px'}
                height={'300px'}
                showLegend
                legendItems={legendItems}
                xAxisTitle={'Avg Test Scores'}
            />
        </div>
    );
};

export default AverageScores;
