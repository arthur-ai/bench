import React, { ReactElement, useRef, useState } from "react";
import { useFela } from "react-fela";
import secondary from "resources/colors/Arthur/secondary";
import TableCell from "./TableCell";
import Icon, { EIconType } from "../../Icon";
import { TableCellProps } from "../typings";
import useOnClickOutside from "api/useOnClickOutside";

type ExpandableTableCellProps = {
    limit: number | boolean; // character count or scrollable flag
    content: string | ReactElement | null;
    tableCellProps: TableCellProps;
};

const styles = {
    close: {
        position: "absolute",
        right: "16px",
        top: "8px",
    },
    fullText: {
        padding: "24px",
        position: "absolute",
        width: "420px",
        background: "#fff",
        border: "1px solid #fff",
        fontSize: "14px",
        lineHeight: "28px",
        zIndex: 3,
        boxShadow: "0px 4px 12px rgba(26, 0, 22, 0.24)",
        wordWrap: "break-word",
    },
    expander: {
        position: "relative",
        margin: "-12px",
        padding: "12px",
        "&:hover div": {
            display: "block",
        },
    },
    expandButton: {
        position: "absolute",
        display: "none",
        right: "8px",
        bottom: "8px",
        padding: "2px 4px",
        borderRadius: "2px",
        background: secondary.variant.grey.active,
        cursor: "pointer",
    },
};

const ExpandableTableCell = (props: ExpandableTableCellProps) => {
    const { css } = useFela();
    const { content, limit, tableCellProps } = props;
    const [displayModal, setdisplayModal] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    useOnClickOutside(containerRef, () => setdisplayModal(false));

    const clickBlocker = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const expandText = (e: React.MouseEvent) => {
        clickBlocker(e);
        setdisplayModal(true);
    };

    const collapseText = (e: React.MouseEvent) => {
        clickBlocker(e);
        setdisplayModal(false);
    };

    const btnWrapper = (a: any) => (
        <div className={css(styles.expander)}>
            {a}
            <div tabIndex={0} role='button' onClick={expandText} className={css(styles.expandButton)}>
                <Icon icon={EIconType.EXPAND} size={16} testId='expandableCellOpenIcon' />
            </div>
        </div>
    );

    const renderContent = () => {
        let result = content;

        if (typeof content === "string") {
            // Ensure limit is a number.
            // Random default should always be overwritten by required prop
            let charLimit = 256;

            if (typeof limit === "number") {
                charLimit = limit;
            }

            if (content.length > charLimit) {
                result = btnWrapper(`${content.substring(0, charLimit)}...`);
            }
        } else {
            if (typeof limit === "boolean" && limit) {
                result = btnWrapper(<div style={{ maxHeight: "150px", overflow: "clip" }}>{content}</div>);
            }
        }

        return result;
    };

    return (
        <TableCell {...tableCellProps}>
            {renderContent()}
            {displayModal && (
                <div className={css(styles.fullText)} ref={containerRef} onClick={clickBlocker}>
                    <Icon
                        clickHandler={collapseText}
                        size={24}
                        className={css(styles.close)}
                        icon={EIconType.CANCEL_ROUND}
                        testId='expandableCellCloseIcon'
                    />
                    {content}
                </div>
            )}
        </TableCell>
    );
};

export default ExpandableTableCell;
