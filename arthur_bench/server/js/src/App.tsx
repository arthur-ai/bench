import React, { useEffect } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { useFela, FelaStyle } from 'react-fela';
import ArthurRoutes from './routes';
import Layout from '@compound/Layout/Layout';


function App() {
    const { renderer, theme }: any = useFela();
    const bodyStyle: FelaStyle<any, any> = {
        backgroundColor: theme.bkg_1,
        color: theme.color_2,
        margin: 0,
        fontFamily: theme.font_1,
        height: '100%',
    };
    useEffect(() => {
        renderer.renderStatic(bodyStyle, 'html,body');
    }, [renderer]);

    return (
        <main>
            <BrowserRouter>
                <Layout>
                    <ArthurRoutes />
                </Layout>
            </BrowserRouter>
        </main>
    );
}

export default App;
