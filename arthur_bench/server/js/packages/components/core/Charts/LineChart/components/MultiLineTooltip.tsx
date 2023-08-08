import React from 'react';
import { CssFunction } from 'react-fela';
import { dateLabelFormatter } from 'utils/format/date-label-formatter';
import { ETimeInterval } from '../../../../compound/ModeSelector/ModeSelector';
import { styles } from './styles';

export type TooltipDataPoint = {
    data: Array<string>;
    color: string;
    seriesName: string;
    axisValue: string;
};

type Props = {
    event: TooltipDataPoint[];
    css: CssFunction<{}, {}>;
    data: any;
    timeInterval: ETimeInterval;
};

const MultiLineTooltip = ({ event, css, data, timeInterval }: Props) => {
    const timeStamp = event[0]?.axisValue;
    const dateDisplay = dateLabelFormatter(timeStamp, timeInterval);
    return (
        <div>
            {timeStamp && <div style={styles.tooltipDate}>{dateDisplay}</div>}
            {event.map((dataPoint: TooltipDataPoint, i: number) => {
                return (
                    <div
                        key={dataPoint.seriesName}
                        style={styles.tooltipDatapoint}
                    >
                        <span
                            style={{ backgroundColor: dataPoint.color }}
                            className={css(styles.tooltipDataColor)}
                        />
                        <span style={styles.tooltipDatapointLabel}>
                            {data[i].name}:
                        </span>{' '}
                        {parseFloat(dataPoint.data[1]).toFixed(7)}
                    </div>
                );
            })}
        </div>
    );
};

export default MultiLineTooltip;
