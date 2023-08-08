import React from 'react';
import { State } from 'arthur-redux';
import { connect } from 'react-redux';
import { RendererProvider, ThemeProvider } from 'react-fela';
import { I18nextProvider } from 'react-i18next';

import { compose } from 'ui/helpers/compose';
import renderer from '../renderer';
import themeLight from 'resources/theme/light';
import { get } from 'utils/helpers';
import i18n from '../copy/initCopy';


import App from '../App';


const Skin = ({ felaTheme }: any) => {
    return (
        <RendererProvider renderer={renderer}>
            <ThemeProvider
                theme={get('bkg_1')(felaTheme) ? felaTheme : themeLight}
            >
                <I18nextProvider i18n={i18n}>
                    <App />
                </I18nextProvider>
            </ThemeProvider>
        </RendererProvider>
    );
};

export default compose(
    connect((state: State) => {
        return {
            felaTheme: get('skin.skin.value')(state),
        };
    })
)(Skin);
