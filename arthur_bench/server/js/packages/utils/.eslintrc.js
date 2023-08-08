module.exports = {
    root: true,
    extends: ['custom', 'plugin:jest/recommended'],
    plugins: ['jest'],
    ignorePatterns: ['jest.config.ts'],
    globals: {
        NodeJS: true,
    },
};
