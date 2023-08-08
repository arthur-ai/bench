import React from 'react';
import styles from './styles';
import { Link } from 'react-router-dom';
import { useFela } from 'react-fela';

type TBreadcrumbItem = {
    link?: string;
    label: string;
};

type TBreadcrumbItems = Array<TBreadcrumbItem>;

type Props = {
    items: TBreadcrumbItems;
    testId?: string;
};

const Breadcrumbs = (props: Props) => {
    const { items, testId = 'Breadcrumbs--Root' } = props;
    const { css } = useFela();

    const isLastItem = (index: number) => items.length === index + 1;

    const renderLink = (item: TBreadcrumbItem) => (
        <Link className={css(styles.link)} to={item.link!}>
            {item.label}
        </Link>
    );

    const renderItem = (item: TBreadcrumbItem, index: number) => {
        const isLast = isLastItem(index);

        return (
            <div key={item.label} className={css(styles.item)}>
                {item.link && !isLast ? (
                    renderLink(item)
                ) : (
                    <span className={css(styles.label(isLast))}>
                        {item.label}
                    </span>
                )}
                {isLast ? null : <span className={css(styles.divider)}>/</span>}
            </div>
        );
    };

    const renderItems = () => (
        <div data-testid={testId} className={css(styles.root)}>
            {items.map(renderItem)}
        </div>
    );

    return items.length ? renderItems() : null;
};

export default Breadcrumbs;
