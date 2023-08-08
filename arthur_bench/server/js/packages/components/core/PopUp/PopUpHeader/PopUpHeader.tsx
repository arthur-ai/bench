import React from 'react';
import { useFela } from 'react-fela';
import Icon, { EIconType } from '../../Icon';
import styles from './styles';

type TPopUpHeaderProps = {
    title: string;
    onClick: any;
};
const PopUpHeader = (props: TPopUpHeaderProps) => {
    const { title, onClick } = props;
    const { css } = useFela();
    return (
        <div className={css(styles)}>
            <p>{title}</p>
            <Icon
                icon={EIconType.CLOSE_CIRCLE}
                style={{ cursor: 'pointer' }}
                color={'black'}
                size={20}
                clickHandler={onClick}
            />
        </div>
    );
};

export default PopUpHeader;
