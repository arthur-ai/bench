import { languages } from './constants';

export type LanguageObjType = (typeof languages)[0];

export enum ELngId {
    ENGLISH = 'en',
    SPANISH = 'es',
    JAPANESE = 'jp',
}

type TLngId = ELngId.ENGLISH | ELngId.SPANISH | ELngId.JAPANESE;

export type TLng = {
    id: TLngId;
    name: string;
};
