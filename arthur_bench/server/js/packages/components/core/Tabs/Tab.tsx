import React from 'react';
import { tabStyles } from './styles';
import { useFela } from 'react-fela';
import { ETabsStyle } from './Tabs';

export type TTab = {
    id: string;
    label: string;
    disabled?: boolean;
};

export type Props = {
    tab: TTab;
    selected?: boolean;
    style?: ETabsStyle;
    onClick: (tabId: string) => void;
};

const Tab = (props: Props) => {
    const { tab, selected, onClick, style } = props;
    const { css, theme } = useFela();

    const handleTabClick = () => {
        if (!tab.disabled) {
            onClick(tab.id);
        }
    };

    return (
        <div
            role='button'
            tabIndex={-1}
            onMouseDown={handleTabClick}
            className={css(
                tabStyles.root(style),
                selected ? tabStyles.selected(theme, style) : {},
                tab.disabled ? tabStyles.disabled(style) : {}
            )}
        >
            {tab.label}
        </div>
    );
};

export default Tab;
