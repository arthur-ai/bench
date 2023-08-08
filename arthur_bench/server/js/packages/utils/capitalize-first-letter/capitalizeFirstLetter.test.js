const { capitalizeFirstLetter } = require('./index');

describe('Capitalize First Letter', () => {
    test('Simple capitalization test', () => {
        expect(capitalizeFirstLetter('arthur')).toBe('Arthur');
    });

    test('Capitalization of one letter', () => {
        expect(capitalizeFirstLetter('a')).toBe('A');
    });

    test('null returns null', () => {
        expect(capitalizeFirstLetter(null)).toBe(null);
    });
});
