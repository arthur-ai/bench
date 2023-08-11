import React from 'react';
import Tab, { TTab } from './Tab';
import { useFela } from 'react-fela';
import styles from './styles';

export enum ETabsStyle {
    BUTTONS,
}

type Props = {
    tabs: TTab[];
    style?: ETabsStyle;
    selectedTabId: string;
    styles?: any;
    onTabClick: (tabId: string) => void;
};

const Tabs = (props: Props) => {
    const { selectedTabId, tabs, onTabClick, style } = props;
    const { css } = useFela();

    const handleTabClick = (tabId: string) => {
        onTabClick(tabId);
    };

    const renderTabs = () =>
        tabs.map((tab: TTab) => (
            <Tab
                style={style}
                key={tab.id}
                selected={tab.id === selectedTabId}
                onClick={handleTabClick}
                tab={tab}
            />
        ));

    return tabs.length ? (
        <div className={css(styles.root(style), props.styles)}>
            {renderTabs()}
        </div>
    ) : null;
};

export default Tabs;
