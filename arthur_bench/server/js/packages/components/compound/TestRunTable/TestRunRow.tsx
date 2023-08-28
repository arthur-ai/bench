import React, { useState } from 'react';
import {TableCell, TableRow} from '../../core/Table';
import styles, {cellStyles} from './styles';
import {useFela} from 'react-fela';
import {Run} from 'arthur-redux/slices/testSuites/types';
import {parseAndFormatDate} from '../InsightHeadline/InsightHeadline';
import {Button} from '../../core/Button';
import {EIconType} from "../../core/Icon";
import {useNavigate} from "react-router-dom";

type TRowProps = {
    testRun: Run;
    testSuiteId: string
};


const TestRunRow = ({ testRun, testSuiteId }: TRowProps) => {
    const [showActions, setShowActions] = useState(false);
    const { css } = useFela();
    const  navigate  = useNavigate();
    
    return (
        <TableRow
            className={css(styles.row)}
            onMouseEnter={() => setShowActions(true)}
            onMouseLeave={() => setShowActions(false)}
        >
          {/* hide checkbox until we implement compare functionality
           <TableCell className={css(cellStyles())}>
                <input type='checkbox' />
            </TableCell>*/}
            <TableCell className={css(cellStyles('200px'))}>
                {parseAndFormatDate(testRun.updated_at)}
            </TableCell>
            <TableCell className={css(cellStyles('500px'))}>
                <div className={css(styles.nameCell)}>
                    <div>{testRun.name}</div>
                    {showActions && (
                            <Button
                                isLink={true}
                                text={'VIEW'}
                                iconStart={EIconType.EXTERNAL_LINK}
                                clickHandler={() =>
                                    navigate(
                                        `/bench/${testSuiteId}/runs/${testRun.id}`
                                    )
                                }
                            />
                    )}
                </div>
            </TableCell>

            <TableCell className={css(cellStyles())}>
                {testRun.avg_score.toFixed(2)}
            </TableCell>
        </TableRow>
    );
};

export default TestRunRow;
