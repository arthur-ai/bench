import { Region } from './types';

import { comparatorLangMap } from 'api/comparators.types';

export const buildPhrasing = (region: Region): string[] => {
    const phrasing: string[] = [];
    const regionsArray = Object.keys(region);
    regionsArray.forEach((attr: string) => {
        const attrCondition = region[attr];
        const comparators = Object.keys(attrCondition);
        comparators.forEach((comparator: string) => {
            const value = attrCondition[comparator];
            const phrase = `${attr} ${comparatorLangMap[comparator]} ${value}`;
            phrasing.push(phrase);
        });
    });

    return phrasing;
};
