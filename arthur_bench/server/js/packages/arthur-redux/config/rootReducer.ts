import { combineReducers } from 'redux';
import Skin from '../slices/skin/skin.reducers';
import { testSuitesReducer } from '../slices/testSuites/reducers';

export default combineReducers({
    testSuites: testSuitesReducer,
    skin: Skin,
});
