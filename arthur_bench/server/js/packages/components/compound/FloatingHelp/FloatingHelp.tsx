import React, { useEffect, useState } from 'react';
import { useFela } from 'react-fela';
import { useTranslation } from 'react-i18next';

import primary from 'resources/colors/Arthur/primary';
import checkIfEnter from 'utils/keypress-enter';

import Icon, { EIconType } from '../../core/Icon';
import HelpTile, { HelpTileProps } from '../../core/HelpTile';
import * as styles from './styles';
import { Button } from '../../core/Button';
import secondary from 'resources/colors/Arthur/secondary';

const INDEPTH_LINK = 'https://github.com/arthur-ai/arthur-sandbox';
const DOCS_LINK = 'https://docs.arthur.ai/index.html';
const EMAIL_LINK = 'mailto:support@arthur.ai';
const ELEMENT_EMAIL_LINK = 'mailto:feedback@arthur.ai';
const QUICKSTART_LINK =
    'https://docs.arthur.ai/user-guide/arthur_quickstart.html';
const BUTTON_LINK =
    'https://docs.arthur.ai/user-guide/walkthroughs/model-onboarding/index.html';
const PYTHON_LINK = 'https://github.com/arthur-ai/bench';
const BENCH_DOCS_LINK = 'https://docs.arthur.ai/bench/index.html';

interface Props {
    paidUser?: boolean;
}

function FloatingHelp({ paidUser }: Props) {
    const { t } = useTranslation(['common']);
    const { css } = useFela();
    const [open, setOpen] = useState(false);
    const [isBench, setIsBench] = useState(false);

    const togglePanel = () => setOpen(!open);
    const closePanel = () => setOpen(false);
    const handleKeypress = (e: any) => {
        checkIfEnter(e, togglePanel);
    };
    const clickHandler = () => {
        window.open(BUTTON_LINK);
    };
    useEffect(() => {
        window.location.href.includes('bench')
            ? setIsBench(true)
            : setIsBench(false);
    }, [window.location.href]);

    const leftOptions: Array<HelpTileProps> = [
        {
            title: t('onboarding.quickstartExample'),
            description: t('onboarding.tryArthur'),
            link: QUICKSTART_LINK,
            icon: EIconType.EXTERNAL_LINK,
            effort: t('onboarding.uploadEffort', { minutes: '5' }),
        },
        {
            title: t('onboarding.inDepthExample'),
            description: t('onboarding.practiceWithOne'),
            link: INDEPTH_LINK,
            icon: EIconType.EXTERNAL_LINK,
            effort: t('onboarding.uploadEffort', { minutes: '15-20' }),
        },
        {
            title: t('onboarding.uploadOwnModel'),
            description: (
                <div>
                    <div>{t('onboarding.startMonitor')}</div>
                    <br />
                    <Button
                        text={t('button.getStarted')}
                        iconEnd={EIconType.EXTERNAL_LINK}
                        testId='getStartedButton'
                        clickHandler={clickHandler}
                        className={css({ width: '155px' })}
                    />
                </div>
            ),
            link: '',
            icon: undefined,
            effort: '',
        },
    ];

    const rightOptions: Array<HelpTileProps> = [
        {
            title: t('onboarding.productTour'),
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
            description: t('onboarding.productText'),
            link: '',
            icon: EIconType.ARROW_RIGHT,
            effort: t('onboarding.totalEffort', { minutes: '15-20' }),
            disabled: true,
        },
        {
            title: t('onboarding.arthurDocs'),
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
            description: t('onboarding.learnDetails'),
            link: DOCS_LINK,
            icon: EIconType.EXTERNAL_LINK,
            effort: '',
        },
        {
            title: paidUser
                ? t('onboarding.support')
                : t('onboarding.feedback'),
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
            description: paidUser
                ? t('onboarding.emailUs')
                : t('onboarding.hearFromYou'),
            link: paidUser ? EMAIL_LINK : ELEMENT_EMAIL_LINK,
            icon: EIconType.EXTERNAL_LINK,
            effort: '',
            disabled: paidUser,
        },
    ];

    const benchOptions: HelpTileProps[] = [
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
                    {isBench ? (
                        <div
                            className={css({
                                ...styles.columnStyle,
                                boxShadow:
                                    'inset -1px 0px 0px rgba(26, 0, 22, 0.1)',
                            })}
                        >
                            {benchOptions.map((o) => (
                                <div key={o.title}>
                                    <HelpTile {...o} />
                                </div>
                            ))}
                        </div>
                    ) : (
                        <>
                            <div
                                className={css({
                                    ...styles.columnStyle,
                                    boxShadow:
                                        'inset -1px 0px 0px rgba(26, 0, 22, 0.1)',
                                })}
                            >
                                <h4>{t('onboarding.getStarted')}</h4>
                                {leftOptions.map((o) => (
                                    <div key={o.title}>
                                        <HelpTile {...o} />
                                    </div>
                                ))}
                            </div>
                            <div className={css(styles.columnStyle)}>
                                <h4>{t('onboarding.addHelp')}</h4>
                                {rightOptions.map((o) => (
                                    <div key={o.title}>
                                        <HelpTile {...o} />
                                    </div>
                                ))}
                            </div>
                        </>
                    )}
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
