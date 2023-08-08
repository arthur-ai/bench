import configureProductionStore from './configureStore.prod';
const currentEnvironment = process.env.NODE_ENV;

const environmentConfigs: Record<string, any> = {
    production: configureProductionStore,
};

if (currentEnvironment && !(currentEnvironment in environmentConfigs)) {
    throw new Error('Unrecognized node environment');
}

export default currentEnvironment
    ? environmentConfigs[currentEnvironment]
    : null;
