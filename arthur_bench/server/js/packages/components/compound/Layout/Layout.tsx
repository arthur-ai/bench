import React, { FunctionComponent } from 'react';
import { useFela } from 'react-fela';
import styles from './styles';
import FloatingHelp from '../FloatingHelp/FloatingHelp'

interface Props {
    children: React.ReactNode;
}

const Layout: FunctionComponent<Props> = ({ children }) => {
    const {css} = useFela();

    return (
        <div className={css(styles.body)}>
            <div>{children}</div>
            <FloatingHelp/>
            <div className={css(styles.footer)}>
                Learn more at &nbsp; <a href="https://arthur.ai" className={css(styles.link)} target="_blank"> arthur.ai </a>
                &nbsp; or check out &nbsp; <a href="https://bench.readthedocs.io/en/latest/index.html" className={css(styles.link)} target="_blank"> Bench Docs </a>
            </div>
        </div>
    );
};

export default Layout;
