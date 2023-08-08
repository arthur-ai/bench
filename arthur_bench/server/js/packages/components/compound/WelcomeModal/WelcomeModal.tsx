import React, { useState } from 'react';
import Modal from '../../core/Modal/Modal';
import HelpTile from '../../core/HelpTile';
import { useTranslation } from 'react-i18next';
import { iconBox } from '../FloatingHelp/styles';
import Icon, { EIconType } from '../../core/Icon';
import secondary from 'resources/colors/Arthur/secondary';
import { useFela } from 'react-fela';
import styles from './styles';
import Welcome from 'resources/images/welcome.svg';
import Logo from 'resources/images/Arthur_Logo_PBW.svg';
import primary from 'resources/colors/Arthur/primary';

const PYTHON_LINK = 'https://github.com/arthur-ai/bench';
const BENCH_DOCS_LINK = 'https://docs.arthur.ai/bench/index.html';
const WelcomeModal = () => {
    const [showModal, setShowModal] = useState<boolean>(true);
    const { t } = useTranslation();
    const { css } = useFela();
    return (
        <Modal showModal={showModal} setShowModal={setShowModal}>
            <div className={css(styles.modal)}>
                <div className={css(styles.left)}>
                    <div className={css(styles.title)}>
                        <h2>Welcome to</h2>{' '}
                        <img src={Logo} alt={'Arthur Logo'} />
                    </div>
                    <span>
                        Here are some helpful resources for you to get started
                    </span>

                    <div className={css(styles.helpTiles)}>
                        <HelpTile
                            title={t('benchResources.python')}
                            description={t('benchResources.pythonText')}
                            link={PYTHON_LINK}
                            titleIcon={
                                <div
                                    className={css({
                                        ...iconBox,
                                        backgroundColor: secondary.lightBlue,
                                    })}
                                >
                                    <Icon
                                        icon={EIconType.DOCUMENTATION}
                                        size={24}
                                        color={secondary.blue}
                                    />
                                </div>
                            }
                            icon={EIconType.EXTERNAL_LINK}
                        />
                        <HelpTile
                            title={t('onboarding.arthurDocs')}
                            description={t('onboarding.learnDetails')}
                            link={BENCH_DOCS_LINK}
                            titleIcon={
                                <div
                                    className={css({
                                        ...iconBox,
                                        backgroundColor: '#F4E8FC', // Faking Opacity
                                    })}
                                >
                                    <Icon
                                        icon={EIconType.CODE_BRIEFCASE_FILLED}
                                        size={24}
                                        color={secondary.purple}
                                    />
                                </div>
                            }
                            icon={EIconType.EXTERNAL_LINK}
                        />
                    </div>
                </div>
                <div className={css(styles.imageContainer)}>
                    <img src={Welcome} alt={'welcome to bench'} />
                    <Icon
                        size={24}
                        icon={EIconType.CLOSE_CIRCLE}
                        color={primary.white}
                        className={css(styles.closeButton)}
                        clickHandler={() => setShowModal(false)}
                    />
                </div>
            </div>
        </Modal>
    );
};

export default WelcomeModal;
