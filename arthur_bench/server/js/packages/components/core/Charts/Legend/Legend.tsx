import React from 'react';
import { useFela } from 'react-fela';
import { styles } from './styles';

export enum ELegendItemShape {
    CIRCLE = 'circle',
    SQUARE = 'square',
    LINE = 'line',
    DASH = 'dash',
}

export type LegendItem = {
    color: string;
    name: string;
    subtitle?: string;
    shape: ELegendItemShape;
};

export type LegendItems = Array<LegendItem>;

type LegendProps = {
    items: LegendItems;
};

const Legend = (props: LegendProps) => {
    const { css } = useFela();

    return (
        <div className={css(styles.root)}>
            {props.items.map((item: LegendItem) => (
                <div className={css(styles.itemRoot)}>
                    <span
                        className={css(
                            styles.itemBase(item.color),
                            styles.item[item.shape]
                        )}
                    />
                    <div className={css(styles.itemHolder)}>
                        <span>{item.name}</span>
                        {item.subtitle && (
                            <span className={css(styles.subtitle)}>
                                {item.subtitle}
                            </span>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Legend;
