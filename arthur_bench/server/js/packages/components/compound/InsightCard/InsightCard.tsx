import React, { useMemo, useState } from 'react';
import { useFela } from 'react-fela';
import { useTranslation } from 'react-i18next';
import arthurAxios from 'arthur-axios';

import TooltipComponent from '../../core/Tooltip/Tooltip';

import { InsightProps } from './types';
import StyledSelect from '../../core/StyledSelect/StyledSelect';
import { Button, EButtonVariation } from '../../core/Button';
import { buildPhrasing } from './utils';
import styles, { statusDropdownStyles } from './styles';

const InsightCard = ({ insight, openInferences }: InsightProps) => {
    const { metric_type, metric_value, region } = insight;
    const { css } = useFela();
    const { t } = useTranslation(['common']);
    const [status, setStatus] = useState(insight.status);

    const statusList = useMemo(
        () => [
            { id: 'new', name: t('insightCard.new') },
            { id: 'acknowledged', name: t('insightCard.acknowledged') },
        ],
        []
    );

    const handleSetStatus = (option: any) => {
        arthurAxios
            .patch(
                `/api/v3/models/${insight.model_id}/insights/${insight.id}`,
                {
                    status: option.id,
                }
            )
            .then(() => setStatus(option.id));
    };

    const phrasing = buildPhrasing(region);
    const phraseList = (start: number, stop?: number) => {
        return phrasing
            .slice(start, stop)
            .map((item) => (
                <p className={css(styles.attributeLogic)}>{item}</p>
            ));
    };

    return (
        <div className={css(styles.container)}>
            <div className={css(styles.topRow)}>
                <span className={css(styles.box)}>
                    {metric_type + ': ' + metric_value.toFixed(4)}
                </span>
                {/* to do: get actual inference count*/}
                <span className={css(styles.box)}>
                    Inferences Count: {insight.inference_count}
                </span>
            </div>
            <div>
                {phraseList(0, 4)}
                {phrasing.length > 4 && (
                    <TooltipComponent
                        direction={'right'}
                        content={phraseList(4)}
                    >
                        <p className={css(styles.showAdditional)}>
                            {`+ ${phrasing.length - 4} more`}
                        </p>
                    </TooltipComponent>
                )}
            </div>
            <div className={css(styles.bottomRow)}>
                <Button
                    variation={EButtonVariation.SECONDARY}
                    text={t('insightCard.viewInferences')}
                    style={{ width: '180px' }}
                    clickHandler={() => openInferences(insight)}
                    //onClick: switch to insights deep dive with filter applied
                ></Button>
                <StyledSelect
                    items={statusList}
                    changeHandler={handleSetStatus}
                    selectedItem={statusList.find((x) => x.id === status)}
                    filled={true}
                    customStyles={statusDropdownStyles}
                    large={true}
                ></StyledSelect>
            </div>
        </div>
    );
};

export default InsightCard;
