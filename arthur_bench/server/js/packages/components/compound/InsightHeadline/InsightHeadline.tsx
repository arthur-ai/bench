import { format, parseISO } from 'date-fns';
import React, { ReactNode, useState } from 'react';
import { useFela } from 'react-fela';
import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import { capitalizeFirstLetter } from 'utils/capitalize-first-letter';
import Icon, { EIconType } from '../../core/Icon';
import { styles } from './styles';

export type InsightGroup = {
    metricGroup: string;
    threshold: number;
    timestamp: string;
    startTime?: string;
    endTime?: string;
    batchId?: string;
    subGroupCount?: number;
};

export const parseAndFormatDate = (dateIsoString: string) => {
    return format(parseISO(dateIsoString), 'LLL d, y, hh:mm');
};

const InsightsHeadline = ({
    insightGroup,
    children,
}: {
    insightGroup: InsightGroup;
    children?: ReactNode;
}) => {
    const [isOpen, setIsOpen] = useState(false);
    const { css } = useFela();

    const renderMessage = (insightGroup: InsightGroup) => {
        return (
            <p className={css(styles.message)}>
                <strong>
                    {capitalizeFirstLetter(insightGroup.metricGroup)}
                </strong>{' '}
                has fallen{' '}
                <strong>below {insightGroup.threshold * 100}%</strong> in{' '}
                <strong>{insightGroup.subGroupCount} subgroups</strong>{' '}
                {insightGroup.batchId ? `of batch ${insightGroup.batchId}` : ''}
            </p>
        );
    };

    return (
        <div className={css(styles.root)}>
            <div
                className={css(styles.headlineWrap)}
                role='presentation'
                onClick={() => setIsOpen(!isOpen)}
            >
                <div>
                    <Icon
                        icon={
                            isOpen
                                ? EIconType.CHEVRON_DOWN
                                : EIconType.CHEVRON_RIGHT
                        }
                        size={24}
                        color={primary.raisin}
                    />
                </div>
                <div>
                    <Icon
                        icon={EIconType.LIGHTBULB}
                        size={24}
                        color={secondary.yellow}
                    />
                </div>
                <div>
                    <div className={css(styles.timestamp)}>
                        {insightGroup.startTime && insightGroup.endTime
                            ? `${parseAndFormatDate(
                                  insightGroup.startTime
                              )} - ${parseAndFormatDate(insightGroup.endTime)}`
                            : `${parseAndFormatDate(insightGroup.timestamp)}`}
                    </div>
                    <div>{renderMessage(insightGroup)}</div>
                </div>
            </div>
            <div>{isOpen && children ? children : null}</div>
        </div>
    );
};

export default InsightsHeadline;
