import React from 'react';
import BarChart from './BarChart';
import { EAxis, EChartsColorBy, TMarkAreaData } from '../constants';
import { ELegendItemShape } from '../Legend/Legend';
import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';

export default {
    title: 'Arthur/Core/Chart/Bar',
    component: BarChart,
};

const data0 = { name: '1', data: { Third: 18, Fourth: 4 } };
const data1 = {
    name: '1',
    data: { First: 8, Second: 20, Third: 18, Fourth: 4 },
};
const data2 = {
    name: '2',
    data: { First: 4, Second: 16, Third: 9, Fourth: 8 },
};

const markArea = {
    axis: EAxis.Y,
    data: [-15, 15],
} as TMarkAreaData;

const legendItem1 = {
    name: 'Young (Baseline)',
    color: primary.eggplant,
    shape: ELegendItemShape.DASH,
};

const legendItem2 = {
    name: 'Within Threshold',
    color: '#FFBF00',
    shape: ELegendItemShape.SQUARE,
};

const legendItem3 = {
    name: 'Over Threshold',
    color: '#2D78CB',
    shape: ELegendItemShape.SQUARE,
};

const markLine = { yAxis: 10 };
const markLineOrange = { yAxis: 10, lineStyle: { color: primary.purple } };
const markLinePurple = { yAxis: 6, lineStyle: { color: secondary.orange } };

export const Default = () => (
    <BarChart
        graphData={[data1]}
        barWidth='40%'
        xAxisTitle='Segments'
        yAxisTitle='Disparity'
    />
);

export const MultipleSeriesAndLine = () => (
    <BarChart
        legendItems={[legendItem1, legendItem2, legendItem3]}
        markLine={[markLine]}
        colorBy={EChartsColorBy.SERIES}
        graphData={[
            { ...data1, color: '#FFBF00' },
            { ...data2, color: '#2D78CB' },
        ]}
        xAxisTitle='Segments'
        barWidth='50px'
        yAxisTitle='Disparity'
    />
);

export const MultipleSeriesAndLineStacked = () => (
    <BarChart
        legendItems={[legendItem1, legendItem2, legendItem3]}
        markLine={[markLine]}
        colorBy={EChartsColorBy.SERIES}
        graphData={[
            { ...data1, color: '#FFBF00' },
            { ...data2, color: '#2D78CB' },
        ]}
        xAxisTitle='Segments'
        barWidth='50px'
        yAxisTitle='Disparity'
        stacked
    />
);

export const MultipleLinesAndArea = () => (
    <BarChart
        markLine={[markLinePurple, markLineOrange]}
        graphData={[data1]}
        markArea={markArea}
        barWidth='40%'
        xAxisTitle='Segments'
        yAxisTitle='Disparity'
    />
);

export const WithNegativeValue = () => (
    <BarChart
        legendItems={[legendItem1, legendItem2, legendItem3]}
        markLine={[{ yAxis: 0 }]}
        markArea={markArea}
        colorBy={EChartsColorBy.DATA}
        graphData={[data0]}
        xAxisTitle='Segments'
        yAxisTitle='Disparity'
    />
);
