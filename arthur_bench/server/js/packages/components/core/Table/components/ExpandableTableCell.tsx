import TableCell from './TableCell';
import secondary from 'resources/colors/Arthur/secondary';
import React, {useRef, useState} from 'react';
import Icon, { EIconType } from '../../Icon';
import { useFela } from 'react-fela';
import { TableCellProps } from '../typings';
import useOnClickOutside from "api/useOnClickOutside";

type TExpandableTableCellProps = {
    limit: number;
    text: string;
    tableCellProps: TableCellProps;
}

const styles = {
    close: {
        position: 'absolute',
        right: '16px',
        top: '8px'
    },
    fullText: {
        padding: '36px 12px 12px 12px',
        position: 'absolute',
        width: '420px',
        background: '#fff',
        border: '1px solid #fff',
        fontSize: '14px',
        lineHeight: '21px',
        zIndex: 3,
        boxShadow: '0px 4px 12px rgba(26, 0, 22, 0.24)',

    },
    expander: {
        position: 'relative',
        margin: '-12px',
        padding: '12px',
        '&:hover div': {
            display: 'block',
        }
    },
    expandButton: {
        position: 'absolute',
        display: 'none',
        right: '8px',
        bottom: '8px',
        padding: '2px 4px',
        borderRadius: '2px',
        background: secondary.variant.grey.active,
        cursor: 'pointer',
    },
}

const ExpandableTableCell = (props: TExpandableTableCellProps) => {
    const { css } = useFela();
    const { text, limit, tableCellProps } = props;
    const [showFullText, setShowFullText] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    useOnClickOutside(containerRef, () => setShowFullText(false));
    const expandText = (e: React.MouseEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        setShowFullText(true);
    };

    const collapseText = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setShowFullText(false);
    };

    const renderText = () => {
        if (text.length > limit) {
            return (
                <div className={css(styles.expander)}>
                    {text.substring(0, limit)}...
                    <div tabIndex={0} role="button" onClick={expandText} className={css(styles.expandButton)}>
                        <Icon icon={EIconType.EXPAND} size={16} />
                    </div>
                </div>
            );
        } else {
            return text;
        }
    };

    return (
        <TableCell {...tableCellProps}>
            {renderText()}
            {showFullText && (
                <div className={css(styles.fullText)} ref={containerRef}>
                    <Icon clickHandler={collapseText} size={24} className={css(styles.close)}
                          icon={EIconType.CANCEL} />
                    {text}
                </div>
            )}
        </TableCell>
    );
};

export default ExpandableTableCell;
