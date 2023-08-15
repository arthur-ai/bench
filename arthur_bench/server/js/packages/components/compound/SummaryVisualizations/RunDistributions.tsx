import React from 'react';
import LineChart from '../../core/Charts/LineChart';
import {
    TDistribution,
    TestRunSummary,
} from 'arthur-redux/slices/testSuites/types';
import { TGraphDataItem } from 'ui/components/core/Charts/LineChart/';
import { useParams } from 'react-router-dom';

const getValues = (summaries: TestRunSummary[], testRunId: string, total: number): TGraphDataItem[] => {
    return summaries.map((summary: TestRunSummary, i: number) => {
        const formattedData: Array<[number, number] | [number]> = summary.histogram.map((t: TDistribution) => {
            const lower = t.low;
            return [parseFloat(lower.toFixed(3)), t.count/total * 100];
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
    const params = useParams();
    const values = getValues(summaries, params.testRunId as string, total);

    return (
        <LineChart
            id={params.testSuiteId}
            graphData={values}
            showLegend
            height={'300px'}
            yAxisTitle={'% of Tests'}
            xAxisTitle={'Avg Test Scores'}
        />
    );
};

export default RunDistributions;
