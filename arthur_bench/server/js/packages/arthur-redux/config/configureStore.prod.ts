import {
    applyMiddleware,
    compose,
    legacy_createStore as createStore,
} from 'redux';
import { apiMiddleware } from 'redux-api-middleware';
import rootReducer from './rootReducer';

export default function configureStore(preloadedState: any) {
    const store = createStore(
        rootReducer,
        preloadedState,
        compose(applyMiddleware(apiMiddleware))
    );

    // expose store when run in Cypress
    if ((window as any).Cypress) {
        (window as any).store = store;
    }

    return store;
}
