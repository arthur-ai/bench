import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import graphs from 'resources/colors/Arthur/graphs';
import { GRAPHIK, ROBOTO } from 'resources/fonts';

export const LOADING_OPTIONS = {
    text: '',
    color: primary.purple,
    textColor: primary.white,
    maskColor: 'transparent',
};

export const rootStyles = {
    position: 'relative',
};

export const emptyMessageStyles = {
    position: 'absolute',
    margin: '40px 150px',
    textAlign: 'center',
    top: 0,
    bottom: 0,
    left: 0,
    right: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: ROBOTO,
    color: primary.raisin,
    fontSize: '14px',
    zIndex: '2',
};

export const secondaryTitle = {
    fontSize: '12px',
    color: primary.raisin,
    fontFamily: GRAPHIK,
    marginTop: '4px',
    textAlign: 'center',
};

export const legendTopContainer = {
    width: '100%',
    display: 'flex',
    justifyContent: 'end',
    paddingRight: '20px',
    boxSizing: 'border-box',
};

export enum EChartsColorBy {
    SERIES = 'series',
    DATA = 'data',
}

export enum EAxis {
    X = 'xAxis',
    Y = 'yAxis',
}

export enum EChartType {
    LINE = 'line',
    BAR = 'bar',
    SCATTER = 'scatter',
}

export const TEXT_COLOR = secondary.variant.eggplant.darker;

export const xAxisDefaults = (formatter: any) => ({
    nameLocation: 'center',
    nameGap: 50,
    type: 'value',
    axisLine: { show: false, lineStyle: { color: graphs.backgrounds.ashGrey } },
    nameTextStyle: {
        color: graphs.backgrounds.raisin,
        fontFamily: GRAPHIK,
    },
    axisLabel: {
        ...(formatter && { formatter }),
        hideOverlap: true,
        color: TEXT_COLOR,
        fontSize: 12,
        fontFamily: ROBOTO,
    },
});

export const yAxisDefaults = (formatter: any) => ({
    nameLocation: 'center',
    nameGap: 40,
    type: 'value',
    axisLine: { show: false, lineStyle: { color: graphs.backgrounds.ashGrey } },
    nameTextStyle: {
        color: graphs.backgrounds.raisin,
        fontFamily: GRAPHIK,
    },
    axisLabel: {
        ...(formatter && { formatter }),
        color: TEXT_COLOR,
        fontSize: 12,
        fontFamily: ROBOTO,
    },
});

export type TMarkAreaData = {
    axis: EAxis;
    data: [number | string, number | string];
};
