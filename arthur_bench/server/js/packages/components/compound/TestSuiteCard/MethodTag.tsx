import { EMethodType } from 'arthur-redux/slices/testSuites/types';
import React from 'react';
import styles from './styles';
import { chartColorsArray } from 'resources/colors/Arthur/graphs';

type Props = {
    name: EMethodType;
};

type Method = {
    name: string;
    color: string;
}
const MethodTag = ({ name }: Props) => {
    let methods: Method[] = []
    for (const value of Object.values(EMethodType)) {
        methods.push({
            name: value.toLowerCase(),
            color: chartColorsArray[methods.length % chartColorsArray.length]
        });
    }

    const renderTag = (name: string) => {
        const method = methods.find((method) => method.name === name);
        if (method) {
            return (
                <div style={styles.tag(method.color)}>
                    {method.name}
                </div>
            );
        }
    };

    return (
        <>
            {renderTag(name)}
        </>
    )
};

export default MethodTag;
