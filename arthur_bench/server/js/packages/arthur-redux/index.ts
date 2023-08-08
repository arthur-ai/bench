import configureStore from './config/configureStore'
import type { State } from './config/state.type';

const store = configureStore();

export { State, store };
