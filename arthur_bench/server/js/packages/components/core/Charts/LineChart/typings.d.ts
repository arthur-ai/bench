import { TMarkAreaData } from '../constants';
import { ELegendItemShape } from '../Legend/Legend';

export type LineSeriesModel = {
    name: string;
    seriesIndex: number;
    option: any;
};

export type TGraphDataItem = {
    name: string;
    data: Array<[number, number] | [number]>;
    subtitle?: string;
    hasMaxValue?: boolean;
    isMaxValuePositive?: boolean;
    isReference?: boolean;
    batchId?: string;
};

export type TLineChartProps = {
    isLoading?: boolean;
    showLegend?: boolean;
    showMaxPoint?: boolean;
    xAxisTitle?: string;
    yAxisTitle?: string;
    height?: string;
    options?: EChartsOption;
    tooltipFormatter?: any;
    xAxisLabelFormatter?: string | ((value: string, index: number) => string);
    yAxisLabelFormatter?: string | ((value: string, index: number) => string);
    markArea?: TMarkAreaData;
    markLine?: MarkLine1DDataItemOption[];
    xAxisData?: string[];
    graphData: Array<TGraphDataItem>;
    hideVerticalLines?: boolean;
    legendItems?: LegendItems;
    xAxisType?: string;
    xSecondaryAxisTitle?: string;
    emptyMessage?: string;
    notMerge?: boolean;
    xAxisLabelOptions?: Record<any, any>;
    xAxisMax?: number | string | Function;
    xAxisMin?: number | string | Function;
    yAxisMax?: number;
    addMarkLineLegendItems?: boolean;
    markLineShape?: ELegendItemShape;
    markPoint?: any;
    markLineColor?: string;
    disableTooltip?: boolean;
    xAxisScale?: boolean;
    showMarkLineLabel?: boolean;
    hideHoverEffects?: boolean;
    smoothData?: boolean;
    hasToolbox?: boolean;
    additionalToolboxItems?: any;
    id?: string;
    dataTestId?: string;
};
