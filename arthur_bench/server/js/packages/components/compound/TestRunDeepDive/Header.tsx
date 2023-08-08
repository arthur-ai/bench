import React from "react";
import {TableCell, TableHeader, TableRow} from "../../core/Table";
import styles from "./styles";
import {useFela} from "react-fela";
import primary from "resources/colors/Arthur/primary";
import secondary from "resources/colors/Arthur/secondary";

const Header = () => {
    const {css} = useFela()
    return (
        <TableHeader>
            <TableRow>
                <TableCell className={css(styles.headerCell(secondary.variant.grey.active))}>
                  <h5>INPUT PROMPTS</h5>
                </TableCell>
                <TableCell className={css(styles.headerCell(secondary.variant.grey.active))}>
                    <h5>REFERENCE OUTPUTS</h5>
                </TableCell>
                <TableCell className={css(styles.headerCell(primary.mint))}>
                    <h5>MODEL OUTPUTS</h5>
                </TableCell>
                <TableCell className={css(styles.headerCell(primary.mint))}>
                    <h5>SCORE</h5>
                </TableCell>
            </TableRow>
        </TableHeader>
    )
};

export default Header
