import React, {useEffect, useState} from 'react';
import {TableCell} from '../../core/Table';
import {headerCell} from './styles';
import {useFela} from 'react-fela';
import Icon, {EIconType} from "../../core/Icon";
import {TColumn} from "./TestRunTable";

const HeaderCell = ({
    column,
    sort,
    setSort,
    selectedSort,
    setSelectedSort,
}: {
    column: TColumn;
    sort: string;
    setSort: (name: string) => void;
    selectedSort: TColumn;
    setSelectedSort: (column: TColumn) => void;

}) => {
    const { css } = useFela();
    const [icon, setIcon] = useState<EIconType>(EIconType.SORT_DEFAULT);

    useEffect(() => {
        if (selectedSort !== column) {
            setIcon(EIconType.SORT_DEFAULT);
        }
    }, [selectedSort, column]);
    const handleSort = () => {
        if (sort === column.asc) {
            setSort(column.desc);
            setIcon(EIconType.SORT_DESC)
        } else  {
            setSort(column.asc);
            setIcon(EIconType.SORT_ASC)
        }

    }
    const handleClick = () => {
        handleSort();
        setSelectedSort(column);
    }

    return (
        <TableCell className={css(headerCell())}>
            <h5>
                {column.name}
                <Icon
                    size={16}
                    icon={icon}
                    clickHandler={handleClick}
                />
            </h5>
        </TableCell>
    );
};


export default HeaderCell;
