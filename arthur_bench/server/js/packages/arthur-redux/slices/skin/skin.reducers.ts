import { SkinState } from './skin.type';
import {
    FETCH_SKIN_REQUEST,
    FETCH_SKIN_RECEIVE,
    FETCH_SKIN_ERROR,
} from './skin.constants';

const defaultState: SkinState = {
    skin: {},
};

type Action = {
    type: string;
    payload?: any;
    error?: any;
    redirectUrl?: string;
};

const Skin = (state: SkinState = defaultState, action: Action): SkinState => {
    switch (action.type) {
        case FETCH_SKIN_REQUEST:
            return {
                ...state,
            };
        case FETCH_SKIN_RECEIVE:
            return {
                ...state,
                skin: action.payload,
            };

        case FETCH_SKIN_ERROR:
            return {
                ...state,
            };

        default:
            return state;
    }
};

export default Skin;
