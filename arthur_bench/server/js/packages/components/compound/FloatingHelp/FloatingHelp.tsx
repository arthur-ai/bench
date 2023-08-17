import React, { useState } from 'react';
import { useFela } from 'react-fela';
import { useTranslation } from 'react-i18next';

import primary from 'resources/colors/Arthur/primary';
import checkIfEnter from 'utils/keypress-enter';

import Icon, { EIconType } from '../../core/Icon';
import HelpTile, { HelpTileProps } from '../../core/HelpTile';
import * as styles from './styles';
import secondary from 'resources/colors/Arthur/secondary';

const PYTHON_LINK = 'https://github.com/arthur-ai/bench';
const BENCH_DOCS_LINK = 'https://docs.arthur.ai/bench/index.html';
const EMAIL_LINK = '';

function FloatingHelp() {
    const { t } = useTranslation(['common']);
    const { css } = useFela();
    const [open, setOpen] = useState(false);

    const togglePanel = () => setOpen(!open);
    const closePanel = () => setOpen(false);
    const handleKeypress = (e: any) => {
        checkIfEnter(e, togglePanel);
    };

    const options: HelpTileProps[] = [
        {
            title: t('benchResources.python'),
            titleIcon: (
                <div
                    className={css({
                        ...styles.iconBox,
                        backgroundColor: '#F4E8FC', // Faking Opacity
                    })}
                >
                    <Icon
                        icon={EIconType.CODE_BRIEFCASE_FILLED}
                        size={24}
                        color={secondary.purple}
                    />
                </div>
            ),
            description: t('benchResources.pythonText'),
            link: PYTHON_LINK,
            icon: EIconType.EXTERNAL_LINK,
        },
        {
            title: t('benchResources.api'),
            titleIcon: (
                <div
                    className={css({
                        ...styles.iconBox,
                        backgroundColor: secondary.lightBlue,
                    })}
                >
                    <Icon
                        icon={EIconType.DOCUMENTATION}
                        size={24}
                        color={secondary.blue}
                    />
                </div>
            ),
            description: t('benchResources.apiText'),
            link: BENCH_DOCS_LINK,
            icon: EIconType.EXTERNAL_LINK,
        },
        {
            title: t('benchResources.support'),
            titleIcon: (
                <div
                    className={css({
                        ...styles.iconBox,
                        backgroundColor: '#FFEAB2', // Faking Opacity
                    })}
                >
                    <Icon
                        icon={EIconType.CHAT_FILLED}
                        size={24}
                        color={secondary.yellow}
                    />
                </div>
            ),
            description: t('benchResources.supportText'),
            link: EMAIL_LINK,
            icon: EIconType.EXTERNAL_LINK,
        },
    ];

    return (
        <div>
            <div className={css(styles.panelStyle(open))}>
                <div className={css(styles.headerStyle)}>
                    <div>{t('onboarding.arthurResources')}</div>
                    <div
                        style={{ cursor: 'pointer' }}
                        onClick={closePanel}
                        onKeyDown={closePanel}
                        tabIndex={0}
                        role='button'
                        data-testid='closePanelIcon'
                    >
                        <Icon icon={EIconType.CANCEL} size={24} />
                    </div>
                </div>
                <div className={css(styles.contentStyle)}>
                    <div
                        className={css({
                            ...styles.columnStyle,
                            boxShadow:
                                'inset -1px 0px 0px rgba(26, 0, 22, 0.1)',
                        })}
                    >
                        {options.map((o) => (
                            <div key={o.title}>
                                <HelpTile {...o} />
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            <div>
                    <span
                        onClick={togglePanel}
                        onKeyDown={handleKeypress}
                        tabIndex={0}
                        role='button'
                        data-testid='floatingHelpBtn'
                    >
                        <Icon
                            icon={EIconType.HELP}
                            color={primary.purple}
                            className={css(styles.iconStyle)}
                            size={36}
                        />
                    </span>
            </div>
        </div>
    );
}

export default FloatingHelp;
