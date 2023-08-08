/* eslint-disable no-unused-vars */

export enum ESearchVariations {
    FLOATING = 'floating',
    NORMAL = 'normal',
}

export type TSearchVariations =
    | ESearchVariations.FLOATING
    | ESearchVariations.NORMAL;

export type SearchProps = {
    searchValue: string;
    setSearchValue: (d: string) => void;
    variation?: TSearchVariations;
    style?: Record<any, any>;
    text?: string;
};
