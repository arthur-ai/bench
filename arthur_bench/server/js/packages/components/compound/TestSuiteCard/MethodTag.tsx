import { EMethodType } from 'arthur-redux/slices/testSuites/types';
import React from 'react';
import primary from 'resources/colors/Arthur/primary';
import secondary from 'resources/colors/Arthur/secondary';
import styles from './styles';

type Props = {
    name: EMethodType;
};
const MethodTag = ({ name }: Props) => {
    const methods = [
        {
            name: EMethodType.BERT,
            color: primary.purple,
        },
        {
            name: EMethodType.SUMMARY,
            color: secondary.orange,
        },
        {
            name: EMethodType.QA,
            color: secondary.yellow,
        },
    ];
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
