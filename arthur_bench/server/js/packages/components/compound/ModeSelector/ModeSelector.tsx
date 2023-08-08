import React from 'react';
import styles from './styles';
import { FelaStyle, useFela } from 'react-fela';
import StyledSelect from '@core/StyledSelect';
import { useTranslation } from 'react-i18next';
import { TSelectItem } from '@core/StyledSelect/StyledSelect';
import Toggle from '@core/Toggle';

export enum EModeInterval {
    SNAPSHOT,
    TIME_SERIES,
}

export enum ETimeInterval {
    MINUTE = 'minute',
    HOUR = 'hour',
    DAY = 'day',
    MONTH = 'month',
    YEAR = 'year',
}

type Props = {
    onChange: (mode: EModeInterval) => void;
    onIntervalChange: (item: TSelectItem) => void;
    selectedInterval: TSelectItem;
    selectedMode: EModeInterval;
    disableToggle?: boolean;
    className?: FelaStyle<{}>;
    isBatch: boolean;
};

export const timeIntervalItems = [
    {
        id: ETimeInterval.MINUTE,
        name: 'Minute',
    },
    {
        id: ETimeInterval.HOUR,
        name: 'Hour',
    },
    {
        id: ETimeInterval.DAY,
        name: 'Day',
    },
    {
        id: ETimeInterval.MONTH,
        name: 'Month',
    },
    {
        id: ETimeInterval.YEAR,
        name: 'Year',
    },
];

const ModeSelector = (props: Props) => {
    const {
        onChange,
        onIntervalChange,
        selectedInterval,
        selectedMode,
        disableToggle,
        className,
    } = props;
    const { css } = useFela();
    const { t } = useTranslation();

    const handleModeChange = (checked: boolean) => {
        onChange(checked ? EModeInterval.SNAPSHOT : EModeInterval.TIME_SERIES);
    };

    const selectTitleRenderer = (i: TSelectItem) =>
        `${t('modeSelector.interval')}: ${t(`dates.${i.id}`)}`;

    const checked = selectedMode === EModeInterval.SNAPSHOT;

    return (
        <div
            data-testid='ModeSelector'
            className={css(styles.root, styles.alignWrap, className || {})}
        >
            <div className={css(styles.main)}>
                <div className={css(styles.alignWrap, styles.titles)}>
                    <div className={css(styles.title)}>
                        {t('modeSelector.timeSeries')}
                    </div>
                    <div className={css(styles.toggleWrap, styles.alignWrap)}>
                        <Toggle
                            disabled={disableToggle}
                            outlined
                            width={22}
                            height={12}
                            isActive={checked}
                            toggleIsActive={handleModeChange}
                        />
                    </div>
                    <div className={css(styles.title)}>
                        {t('modeSelector.snapshot')}
                    </div>
                </div>
                <span className={css(styles.subtitle)}>
                    {t('modeSelector.subtitle')}
                </span>
            </div>
            <StyledSelect
                large
                filled
                titleRenderer={selectTitleRenderer}
                disabled={checked}
                selectedItem={selectedInterval}
                items={timeIntervalItems}
                changeHandler={onIntervalChange}
            />
        </div>
    );
};

export default ModeSelector;
