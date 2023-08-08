const { parseInt: parseIntCustom } = require('./index');

describe('Parse Integer', () => {
    test('Simple string', () => {
        expect(parseIntCustom('10')).toEqual(10);
    });

    test('HEX string', () => {
        expect(parseIntCustom('0x10', 16)).toEqual(16);
    });

    test('Invalid string', () => {
        expect(parseIntCustom('NaN')).toBeNull();
    });

    test('Simple integer', () => {
        expect(parseIntCustom(10)).toEqual(10);
    });

    test('float converted to int', () => {
        expect(parseIntCustom(10.9)).toEqual(11);
    });
});
