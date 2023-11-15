import React, { useEffect, useMemo, useState } from "react";
import merge from "lodash.merge";
import { EChartsOption, EChartsType } from "echarts";
import EChartsReact from "echarts-for-react";
import primary from "resources/colors/Arthur/primary";

import {
    xAxisDefaults,
    yAxisDefaults,
    EChartsColorBy,
    EChartType,
    LOADING_OPTIONS,
    TMarkAreaData,
    emptyMessageStyles,
    rootStyles,
    secondaryTitle,
    legendTopContainer,
} from "../constants";
import graphs, { chartColorsArray } from "resources/colors/Arthur/graphs";
import Legend, { ELegendItemShape, LegendItems } from "../Legend/Legend";
import { MarkLine1DDataItemOption } from "echarts/types/src/component/marker/MarkLineModel";
import { CallbackDataParams } from "echarts/types/dist/shared";
import { useTranslation } from "react-i18next";
import { useFela } from "react-fela";

export type TBarChartData = Record<string, number | string>;

export type TBarChartDataItem = {
    name: string;
    data: TBarChartData;
    color?: string;
    border?: { color: string; type: string; width: number };
    subtitle?: string;
    opacity?: number;
};

export type TBarChartDataItems = Array<TBarChartDataItem>;

type TBarChartProps = {
    id?: string;
    dataTestId?: string;
    isLoading?: boolean;
    xAxisTitle?: string;
    emptyMessage?: any;
    xAxisLabelFormatter?: string | ((value: string, index: number) => string);
    yAxisLabelFormatter?: string | ((value: string, index: number) => string);
    yAxisTitle?: string;
    xSecondaryAxisTitle?: string;
    height?: string;
    tooltip?: any;
    barGap?: number;
    barWidth?: string | number;
    colorBy?: EChartsColorBy;
    onChartClick?: (event: CallbackDataParams, chart: EChartsType) => void;
    options?: EChartsOption;
    markArea?: TMarkAreaData;
    markLine?: MarkLine1DDataItemOption[];
    graphData?: TBarChartDataItems; //setting this as optional for now until there is time to refactor the bench bar chart
    hideVerticalLines?: boolean;
    legendItems?: LegendItems;
    showLegend?: boolean;
    showLegendTop?: boolean;
    useCustomLegendItems?: boolean;
    addMarkLineLegendItems?: boolean;
    yAxisMax?: number;
    stacked?: boolean;
    groupByName?: boolean;
    splitLegendOnChar?: string;
    hasToolbox?: boolean;
    openChartSelections?: () => void | null;
    additionalToolboxItems?: Record<string, Record<string, any>>;
};

const BarChart = (props: TBarChartProps) => {
    const { t } = useTranslation();
    const { css } = useFela();
    const {
        id,
        dataTestId,
        isLoading,
        height = "400px",
        options,
        barWidth = "15%",
        barGap,
        markArea,
        markLine,
        colorBy = EChartsColorBy.DATA,
        onChartClick,
        graphData,
        hideVerticalLines,
        legendItems = [],
        tooltip,
        xAxisLabelFormatter,
        yAxisLabelFormatter,
        emptyMessage,
        showLegend,
        showLegendTop,
        xSecondaryAxisTitle,
        useCustomLegendItems = false,
        addMarkLineLegendItems = false,
        yAxisMax,
        stacked = false,
        groupByName = false,
        hasToolbox = false,
        additionalToolboxItems = {},
    } = props;

    const [stateLegendItems, setLegendItems] = useState<LegendItems>(legendItems);

    useEffect(() => {
        handleAddLegendItems();
    }, [graphData, markLine]);

    const renderEmptyMessage = () => {
        if (graphData) {
            const emptyGraphData = !graphData.length;
            const emptyDataPoint = graphData.every((d) => !Object.keys(d.data).length);
            const zeroesData = graphData.every((d) => Object.values(d.data).every((val) => !val));

            if ((emptyGraphData || emptyDataPoint || zeroesData) && !isLoading) {
                return <div className={css(emptyMessageStyles)}>{emptyMessage || t("charts.emptyMessage")}</div>;
            }
        }

        return null;
    };

    const handleAddLegendItems = () => {
        if (!showLegend || useCustomLegendItems || !graphData) {
            return;
        }

        const allGraphDataKeys: string[] = [];
        graphData.forEach((dataItem: TBarChartDataItem) => {
            allGraphDataKeys.push(...Object.keys(dataItem.data));
        });
        const uniqueDataKeys = Array.from(new Set(allGraphDataKeys));
        const moreLegendItems: LegendItems = [];
        uniqueDataKeys.map((name: string, index: number) => {
            moreLegendItems.push({
                color: chartColorsArray[index],
                name,
                shape: ELegendItemShape.SQUARE,
            });
        });

        if (addMarkLineLegendItems) {
            markLine?.map((dp: any) => {
                moreLegendItems.push({
                    color: dp.lineStyle.color,
                    name: `${dp.name} Ref Data`,
                    shape: ELegendItemShape.DASH,
                });
            });
        }

        setLegendItems([...moreLegendItems, ...legendItems]);
    };

    const tooltipFormatter = (event: { value: number; axisValueLabel: string }[]) => {
        return `<span style='color: rgba(0, 0, 0, 0.6)'>${event[0].axisValueLabel}</span>
                <span style="color: #000000">${event[0].value}</span> `;
    };

    const handleChartClick = (event: CallbackDataParams, chart: EChartsType) => {
        if (onChartClick) {
            onChartClick(event, chart);
        }
    };

    const handleXAxisData = (data: TBarChartDataItems) => {
        if (data?.length) {
            if (groupByName) {
                return data.map((dp: TBarChartDataItem) => dp.name);
            } else {
                return Object.keys(data[0].data);
            }
        } else {
            return [];
        }
    };

    const defaultSeriesOptions = (rw: any, index: number) => ({
        ...(stacked && { stack: "stackbar" }),
        barMinHeight: 1,
        silent: !onChartClick,
        barCategoryGap: "10px",
        barWidth,
        barGap,
        barMaxWidth: 120,
        colorBy,
        type: EChartType.BAR,
        symbolSize: 14,
        itemStyle: {
            color: rw.color,
            barBorderRadius: [2, 2, 0, 0],
            opacity: rw.opacity,
            ...(rw.border && {
                borderType: rw.border.type,
                borderColor: rw.border.color,
                borderWidth: rw.border.width,
            }),
        },
        emphasis: {
            itemStyle: {
                borderWidth: 2,
                shadowColor: "rgba(0, 0, 0, 0.5)",
                shadowBlur: 2,
            },
            focus: "series",
        },
        showSymbol: false,
        ...(!index && {
            ...(markLine && {
                markLine: {
                    silent: true,
                    symbol: "none",
                    lineStyle: { color: primary.raisin, width: 2 },
                    label: { show: false },
                    data: markLine,
                },
            }),
            ...(markArea && {
                markArea: {
                    emphasis: { disabled: true },
                    itemStyle: {
                        color: graphs.backgrounds.ashGrey,
                        opacity: 0.5,
                    },
                    data: [[{ [markArea.axis]: markArea.data[0] }, { [markArea.axis]: markArea.data[1] }]],
                },
            }),
        }),
    });
    const defaultOptions = useMemo(
        () => ({
            ...(hasToolbox
                ? {
                    toolbox: {
                        right: 10,
                        feature: {
                            dataZoom: {
                                yAxisIndex: "none",
                            },
                            ...additionalToolboxItems,
                        },
                    },
                }
                : {}),
            color: chartColorsArray,
            legend: { show: false },
            tooltip: {
                trigger: "axis",
                formatter: tooltip || tooltipFormatter,
                extraCssText: 'font-family: "Mono-Regular"; border-radius: 6px; padding: 4px 12px;',
                borderColor: "transparent",
            },
            xAxis: {
                name: props.xAxisTitle,
                ...xAxisDefaults(xAxisLabelFormatter),
                type: "category",
                axisTick: { show: !hideVerticalLines },
                splitLine: {
                    show: !hideVerticalLines,
                    lineStyle: { color: graphs.backgrounds.ashGrey },
                },
                data: graphData && handleXAxisData(graphData),
            },
            ...(yAxisMax
                ? {
                    yAxis: {
                        max: yAxisMax,
                        name: props.yAxisTitle,
                        ...yAxisDefaults(yAxisLabelFormatter),
                        axisTick: { show: false },
                        splitLine: {
                            lineStyle: { color: graphs.backgrounds.ashGrey },
                        },
                    },
                }
                : {
                    yAxis: {
                        name: props.yAxisTitle,
                        ...yAxisDefaults(yAxisLabelFormatter),
                        axisTick: { show: false },
                        splitLine: {
                            lineStyle: { color: graphs.backgrounds.ashGrey },
                        },
                    },
                }),
            series:
                graphData &&
                (groupByName
                    ? graphData.reduce((final: any, rw: any, index: number) => {
                        Object.keys(rw.data).forEach((key) => {
                            const mappedSeriesData = final.findIndex((dp: any) => dp.name === key);

                            if (mappedSeriesData >= 0) {
                                final[mappedSeriesData].data = [...final[mappedSeriesData].data, rw.data[key]];
                            } else {
                                final.push({
                                    ...defaultSeriesOptions(rw, index),
                                    data: [rw.data[key]],
                                    name: key,
                                });
                            }
                        });

                        return final;
                    }, [])
                    : graphData.map((rw: TBarChartDataItem, index: number) => ({
                        ...defaultSeriesOptions(rw, index),
                        name: rw.name,
                        data: Object.values(rw.data),
                    }))),
        }),
        [graphData]
    );

    return (
        <div style={{ width: "100%" }} className={css(rootStyles)} id={id} data-testid={dataTestId}>
            {renderEmptyMessage()}
            {showLegendTop && !!stateLegendItems?.length && (
                <div className={css(legendTopContainer)}>
                    <Legend items={stateLegendItems} />
                </div>
            )}
            <EChartsReact
                {...props}
                onEvents={{ click: handleChartClick }}
                notMerge={true}
                option={merge(defaultOptions, options)}
                showLoading={isLoading}
                loadingOption={LOADING_OPTIONS}
                style={{ height, width: "100%" }}
                opts={{ renderer: "svg" }}
            />
            {xSecondaryAxisTitle && <div className={css(secondaryTitle)}>{xSecondaryAxisTitle}</div>}
            {showLegend && !!stateLegendItems?.length && <Legend items={stateLegendItems} />}
        </div>
    );
};

export default BarChart;
