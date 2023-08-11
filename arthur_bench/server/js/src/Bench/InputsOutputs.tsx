import React, {useEffect} from "react";
import {useTranslation} from "react-i18next";
import {useFela} from "react-fela";
import styles from './styles';
import InputsOutputsTable from "@compound/InputsOutputsTable/InputsOutputsTable";

const InputsOutputs = () => {
    const {t} = useTranslation(['common']);
    const {css} = useFela();

    return (
        <div className={css(styles.inputOutput)}>
            <div>{t('testSuite.inputsAndOutputs')}</div>
            <InputsOutputsTable/>
        </div>
    )
};


export default InputsOutputs
