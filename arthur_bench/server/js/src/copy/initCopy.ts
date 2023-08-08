import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { Languages } from '../../packages/translations/constants';
import common from '../../packages/translations/en/common.json';
import roundtable from '../../packages/translations/en/roundtable.json';
import overview from '../../packages/translations/en/overview.json';

import commonJp from '../../packages/translations/jp/commonJp.json';
import roundtableJp from '../../packages/translations/jp/roundtableJp.json';

import commonEs from '../../packages/translations/es/commonEs.json';
import roundtableEs from '../../packages/translations/es/roundtableEs.json';

const DefaultLng = Languages.en;

i18n.use(initReactI18next).init({
    lng: DefaultLng,
    fallbackLng: 'en',
    interpolation: { escapeValue: false },
    defaultNS: 'common',
    resources: {
        en: {
            common,
            roundtable,
            overview,
        },
        jp: {
            common: commonJp,
            roundtable: roundtableJp,
        },
        es: {
            common: commonEs,
            roundtable: roundtableEs,
        },
    },
    preload: ['jp', 'en', 'es'],
});

export default i18n;
