export enum Languages {
    en = 'en', // Keep
    jp = 'jp',
    es = 'es',
}
/*
  ... and whatever else we need.
  Good, but suprisingly incomplete reference:
  https://www.ibm.com/docs/en/radfws/9.6.1?topic=overview-locales-code-pages-supported
*/

export const LanguagesNames = {
    [Languages.en]: 'English',
    [Languages.es]: 'Spanish',
    [Languages.jp]: 'Japanese',
};

export const languages = Object.entries(LanguagesNames).map(([id, name]) => ({
    id,
    name,
}));
