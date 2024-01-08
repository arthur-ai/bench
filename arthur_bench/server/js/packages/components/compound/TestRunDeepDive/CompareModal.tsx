import React from "react";
import Modal from "../../core/Modal/Modal";
import Icon, { EIconType } from "../../core/Icon"
import styles from "./styles";
import { useFela } from "react-fela";
import { useTranslation } from "react-i18next";
import { chartColorsArray } from "resources/colors/Arthur/graphs";
import primary from "resources/colors/Arthur/primary";
import secondary from "resources/colors/Arthur/secondary";
import {ComparedTestRuns, Output} from "../../../arthur-redux/slices/testSuites/types";

type props = {
    testCase: ComparedTestRuns;
    showModal: boolean;
    setShowModal: (arg: boolean) => void;
};

const CompareModal = ({ testCase, showModal, setShowModal }: props) => {
    const { t } = useTranslation(["common"]);
    const { css } = useFela();

    const modelDetail = (
        <div className={css(styles.container)}>
            <div className={css(styles.header)}>
                <div>{t("testSuite.viewResults")}</div>
                <Icon
                    icon={EIconType.CANCEL_ROUND}
                    style={{ cursor: "pointer" }}
                    color={primary.black}
                    size={20}
                    clickHandler={() => setShowModal(!showModal)}
                />
            </div>
            <div className={css(styles.header)}>
                <div className={css(styles.headerText)}>
                    {t("testSuite.comparison")} {testCase.outputs.map((output: Output) => output.name).join(", ")}
                </div>
            </div>
            <div className={css(styles.body)}>
                <div className={css(styles.content)}>
                    <div className={css(styles.textBox)}>
                        <div className={css(styles.textBoxHeader(secondary.lightBlue))}>{t("testSuite.inputPrompts")}</div>
                        <div className={css(styles.textBoxBody)}>{testCase.input}</div>
                    </div>
                </div>
                <div className={css(styles.content)}>
                    <div>
                        <div className={css(styles.textBox)}>
                            <div className={css(styles.textBoxHeader(primary.ashGrey))}>{t("testSuite.referenceOutputs")}</div>
                            <div className={css(styles.textBoxBody)}>{testCase.referenceOutput}</div>
                        </div>
                    </div>
                    {testCase.outputs.map((output: Output, index: number) => (
                        <div key={index}>
                            <div className={css(styles.textBox)}>
                                <div className={css(styles.textBoxHeader(chartColorsArray[index]))}>
                                    {output.name}
                                    <div>
                                        {t("testSuite.score")}: {output.score}
                                    </div>
                                </div>
                                <div className={css(styles.textBoxBody)}>{output.output}</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );

    return <Modal children={[modelDetail]} showModal={showModal} setShowModal={setShowModal} />;
};

export default CompareModal;
