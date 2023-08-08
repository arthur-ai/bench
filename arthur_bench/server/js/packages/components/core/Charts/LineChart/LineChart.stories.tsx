import React from 'react';
import LineChart from './LineChart';
import { EAxis, TMarkAreaData } from '../constants';
import { ELegendItemShape } from '../Legend/Legend';
import primary from 'resources/colors/Arthur/primary';
import { MarkerStatisticType } from 'echarts/types/src/component/marker/MarkerModel';
import secondary from 'resources/colors/Arthur/secondary';

export default {
    title: 'Arthur/Core/Chart/Line',
    component: LineChart,
};

const graphData = [
    {
        name: 'Line 1',
        subTitle: 'Reference Group',
        data: [
            [0, 150],
            [1, 230],
            [3, 224],
            [4, 218],
            [5, 135],
        ] as Array<[number, number]>,
    },
];

const markArea = {
    axis: EAxis.Y,
    data: [100, 200],
} as TMarkAreaData;

const legendItem = {
    name: 'Female',
    color: primary.purple,
    shape: ELegendItemShape.LINE,
    subtitle: 'Reference Group',
};

const legendItem2 = {
    name: 'Max',
    color: primary.raisin,
    shape: ELegendItemShape.DASH,
};

const legendItem3 = {
    name: 'Highlighted area',
    color: primary.ashGrey,
    shape: ELegendItemShape.SQUARE,
};

const legendItem4 = {
    name: 'Max Point',
    color: primary.purple,
    shape: ELegendItemShape.CIRCLE,
    subtitle: 'Reference Group',
};

const legendItem5 = {
    name: 'Average',
    color: 'orange',
    shape: ELegendItemShape.DASH,
};

const markLineData = [
    { type: 'average' as MarkerStatisticType, lineStyle: { color: 'orange' } },
    { type: 'max' as MarkerStatisticType },
];

export const Default = () => (
    <LineChart
        legendItems={[legendItem2, legendItem3, legendItem4, legendItem5]}
        showLegend
        hideVerticalLines
        showMaxPoint
        markLine={markLineData}
        graphData={graphData}
        markArea={markArea}
        xAxisTitle='X Axis title'
        yAxisTitle='Y Axis title'
    />
);

export const NoData = () => (
    <LineChart
        hideVerticalLines
        showMaxPoint
        markLine={markLineData}
        graphData={[]}
        markArea={markArea}
        xAxisTitle='X Axis title'
        yAxisTitle='Y Axis title'
    />
);

export const PointOnDist = () => (
    <LineChart
        graphData={graphData}
        xAxisTitle='X Axis title'
        yAxisTitle='Y Axis title'
        markLine={[{ xAxis: 3 }]}
        markLineShape={ELegendItemShape.LINE}
        markPoint={[{ coord: [3, 224] }]}
        markLineColor={primary.purple}
        disableTooltip={true}
    />
);
