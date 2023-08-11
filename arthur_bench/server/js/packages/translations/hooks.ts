import { useTranslation as useTranslationI18 } from 'react-i18next';
import { useCallback } from 'react';
import { LanguageObjType } from './types';

// todo add to the header as a language switcher
export const useTranslation = () => {
    const result = useTranslationI18('common');

    const onChangeLanguage = useCallback(
        (lang: LanguageObjType) => {
            result.i18n.changeLanguage(lang.id);
        },
        [result.i18n]
    );

    return {
        onChangeLanguage,
        translationObj: result,
    };
};
