import React, {useEffect, useState} from 'react';
import merge from 'lodash.merge';
import EChartsReact from 'echarts-for-react';
import {useTranslation} from 'react-i18next';
import {useFela} from 'react-fela';

import graphs, {chartColorsArray} from 'resources/colors/Arthur/graphs';
import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';

import Legend, {ELegendItemShape, LegendItems} from '../Legend/Legend';
import {TGraphDataItem, TLineChartProps} from './typings';
import {
    EChartType,
    emptyMessageStyles,
    LOADING_OPTIONS,
    rootStyles,
    secondaryTitle,
    xAxisDefaults,
    yAxisDefaults,
} from '../constants';
import Loading from '../../../compound/Loading';

const LineChart = (props: TLineChartProps) => {
    const { t } = useTranslation();
    const { css } = useFela();
    const {
        id,
        dataTestId,
        isLoading,
        height = '400px',
        options,
        markArea,
        markLine,
        graphData,
        xAxisData,
        hideVerticalLines,
        tooltipFormatter,
        xAxisLabelFormatter,
        yAxisLabelFormatter,
        legendItems = [],
        showLegend,
        showMaxPoint,
        notMerge,
        emptyMessage,
        xSecondaryAxisTitle,
        xAxisType = 'value',
        xAxisMax,
        xAxisMin,
        yAxisMax,
        addMarkLineLegendItems = false,
        markLineShape = ELegendItemShape.DASH,
        markPoint,
        markLineColor,
        disableTooltip = false,
        xAxisScale = false,
        showMarkLineLabel = false,
        hideHoverEffects = false,
        smoothData = false,
        hasToolbox = false,

        additionalToolboxItems = {},
    } = props;
    const [stateLegendItems, setLegendItems] =
        useState<LegendItems>(legendItems);
    const [graphOptions, setGraphOptions] = useState<Record<
        string,
        any
    > | null>(null);

    const defaultTooltipFormatter = (
        event: { data: [number | string, number | string] | string | number }[]
    ) => {
        let yValue = '';
        let xValue = '';
        const eventDataItem = event[0]?.data;

        if (!Array.isArray(eventDataItem)) {
            xValue = `${eventDataItem || 'no data'}`;
        } else {
            yValue = `${eventDataItem[0] || ''}`;
            xValue = `${eventDataItem[1] || 'no data'}`;
        }

        return `<span style='color: rgba(0, 0, 0, 0.6)'>${yValue}</span>
                <span style="color: #000000">${xValue}</span> `;
    };

    const handleAddLegendItems = () => {
        if (!showLegend || !graphData) {
            return;
        }

        const moreLegendItems: LegendItems = [];

        graphData.forEach((line: TGraphDataItem, index: number) => {
            moreLegendItems.push({
                color: line.name.toLowerCase().includes('baseline') || line.isReference
                    ? graphs.backgrounds.raisin
                    : chartColorsArray[index],
                name: line.name,
                subtitle: graphData[index]?.subtitle || '',
                shape: line.isReference ? ELegendItemShape.DASH : ELegendItemShape.LINE,
            });
        });

        if (addMarkLineLegendItems) {
            markLine?.map((dp: any) => {
                moreLegendItems.push({
                    color: dp.lineStyle.color,
                    name: `${dp.name} Ref Data`,
                    shape: markLineShape,
                });
            });
        }

        setLegendItems([...moreLegendItems, ...legendItems]);
    };

    useEffect(() => {
        setGraphOptions(null);
        const defaultOptions: Record<string, any> = {
                  ...(hasToolbox ? {
                      toolbox: {
                      right: 10,
                      feature: {
                        dataZoom: {
                          yAxisIndex: 'none'
                        },
                        ...additionalToolboxItems,
                      }
                    }
                  } : {}),
            useUTC: true,
            color: chartColorsArray,
                  legend: { show: false },
            ...(!disableTooltip && {
                tooltip: {
                    trigger: 'point',
                    formatter: tooltipFormatter || defaultTooltipFormatter,
                    extraCssText:
                        'font-family: "Mono-Regular"; border-radius: 6px; padding: 4px 12px;',
                    borderColor: 'transparent',
                },
            }),
                        xAxis: {
                axisPointer: {
                    show: true,
                    snap: true,
                    label: {
                        show: false,
                    },
                },
                name: props.xAxisTitle,
                ...xAxisDefaults(xAxisLabelFormatter),
                ...(xAxisData && { data: xAxisData }),
                ...(xAxisMax && { max: xAxisMax }),
                ...(xAxisMin && { min: xAxisMin }),
                scale: xAxisScale,
                type: xAxisType,
                axisTick: { show: !hideVerticalLines },
                splitLine: {
                    show: !hideVerticalLines,
                    lineStyle: { color: graphs.backgrounds.ashGrey },
                },
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

            series: graphData?.map((line: TGraphDataItem, index: number) => ({
                data: line.data,
                name: line.name,
                type: EChartType.LINE,
                symbolSize: 14,
                smooth: smoothData,
                color: chartColorsArray[index],
                emphasis: {
                    itemStyle: {
                        color: 'white',
                        borderColor: chartColorsArray[index] || 'black',
                        borderWidth: 2,
                        shadowColor: 'rgba(0, 0, 0, 0.5)',
                        shadowBlur: 2,
                    },
                },
                symbol: line.data.length === 1 ? 'circle' : 'emptyCircle',
                showSymbol: line.data.length === 1,
                ...(line.isReference
                    ? {
                          lineStyle: {
                              normal: {
                                  color: primary.raisin,
                                  type: 'dashed',
                              },
                          },
                      }
                    : {}),
                ...(showMaxPoint &&
                    line.hasMaxValue && {
                        markPoint: {
                            symbol: 'circle',
                            symbolSize: 8,
                            label: { show: false },
                            data: [
                                {
                                    type: line.isMaxValuePositive
                                        ? 'max'
                                        : 'min',
                                },
                            ],
                            itemStyle: {
                                color: 'red',
                            },
                        },
                    }),
                ...(markPoint ||
                    (hideHoverEffects && {
                        symbolSize: 0,
                        color: [secondary.variant.grey.disabled],
                        emphasis: {
                            itemStyle: {
                                color: secondary.variant.grey.disabled,
                                borderWidth: 0,
                            },
                        },
                        markPoint: {
                            symbol: 'circle',
                            symbolSize: 10,
                            label: { show: false },
                            data: markPoint,
                            itemStyle: {
                                color: primary.white,
                                borderWidth: 2,
                                borderColor: primary.purple,
                            },
                        },
                    })),
                ...(!index && {
                    ...(markLine && {
                        markLine: {
                            silent: true,
                            symbol: 'none',
                            lineStyle: {
                                color: markLineColor || primary.raisin,
                                width: 2,
                                type:
                                    markLineShape === ELegendItemShape.LINE
                                        ? 'solid'
                                        : 'dashed',
                            },
                            label: { show: showMarkLineLabel },
                            data: markLine,
                        },
                    }),
                    ...(markArea && {
                        markArea: {
                            emphasis: { disabled: true },
                            itemStyle: {
                                color: graphs.accents.purple,
                                opacity: 0.1,
                            },
                            data: [
                                [
                                    { [markArea.axis]: markArea.data[0] },
                                    { [markArea.axis]: markArea.data[1] },
                                ],
                            ],
                        },
                    }),
                }),
            })),
        };
        setGraphOptions(defaultOptions);
        handleAddLegendItems();
    }, [graphData, markLine]);

    const renderEmptyMessage = () => {
        const graphEmptyLineData =
            !graphData?.length ||
            graphData.every((line: TGraphDataItem) => !line.data.length);

        if (graphEmptyLineData && !isLoading) {
            return (
                <div className={css(emptyMessageStyles)}>
                    {emptyMessage || t('charts.emptyMessage')}
                </div>
            );
        }

        return null;
    };

    if (!graphOptions) {
        return <Loading />;
    }

    return (
        <div style={{ width: '100%' }} className={css(rootStyles)} id={id} data-testid={dataTestId}>
            {renderEmptyMessage()}

            <EChartsReact
                {...props}
                key={id}
                notMerge={notMerge}
                option={merge(graphOptions, options)}
                showLoading={isLoading}
                loadingOption={LOADING_OPTIONS}
                style={{ height, width: '100%' }}
                opts={{ renderer: 'svg' }}
            />
            {xSecondaryAxisTitle && (
                <div className={css(secondaryTitle)}>{xSecondaryAxisTitle}</div>
            )}
            {showLegend && !!stateLegendItems.length && (
                <Legend items={stateLegendItems} />
            )}
        </div>
    );
};

export default LineChart;
