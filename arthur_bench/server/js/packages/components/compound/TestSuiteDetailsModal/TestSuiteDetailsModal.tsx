import React, { useState } from "react";
import Modal from "../../core/Modal/Modal";
import Icon, { EIconType } from "../../core/Icon";
import styles from "./styles";
import { useFela } from "react-fela";
import { useTranslation } from "react-i18next";
import { DetailedTestSuite } from "arthur-redux/slices/testSuites/types";
import Tabs from "../../core/Tabs";
import GeneralInformationTab from "./GeneralInformationTab";
import ScorerInformationTab from "./ScorerInformationTab";

type props = {
    testSuite: DetailedTestSuite;
    showModal: boolean;
    setShowModal: (arg: boolean) => void;
};

export enum ETab {
    GENERAL_INFORMATION = "GENERAL_INFORMATION",
    SCORER_INFORMATION = "SCORER_INFORMATION",
}

const tabs: { label: string; id: string }[] = [
    {
        label: "General Information",
        id: ETab.GENERAL_INFORMATION,
    },
    {
        label: "Scorer Information",
        id: ETab.SCORER_INFORMATION,
    },
];
const TestSuiteDetailsModal = ({ testSuite, showModal, setShowModal }: props) => {
    const { t } = useTranslation(["common"]);
    const [selectedTab, setSelectedTab] = useState<string>(ETab.GENERAL_INFORMATION);
    const { css } = useFela();
    const modelDetail = (
        <div className={css(styles.container)}>
            <div className={css(styles.header)}>
                <div className={css(styles.title)}>{testSuite.name}</div>
                <Icon
                    icon={EIconType.CLOSE_CIRCLE}
                    style={{ cursor: "pointer" }}
                    color={"black"}
                    size={20}
                    clickHandler={() => setShowModal(!showModal)}
                />
            </div>
            <Tabs tabs={tabs} selectedTabId={selectedTab} onTabClick={setSelectedTab} styles={styles.tabs} />
            <div className={css(styles.body)}>
                {selectedTab === ETab.GENERAL_INFORMATION ? (
                    <GeneralInformationTab testSuite={testSuite} />
                ) : (
                    <ScorerInformationTab testSuite={testSuite} />
                )}
            </div>
        </div>
    );

    return <Modal children={[modelDetail]} showModal={showModal} setShowModal={setShowModal} />;
};

export default TestSuiteDetailsModal;
