const { abbreviateNumber } = require('./index');

const ONE = 1;
const TEN = 10;
const HUNDRED = 100;
const THOUSAND = Math.pow(TEN, 3);
const MILLION = Math.pow(TEN, 6);
const BILLION = Math.pow(TEN, 9);
const TRILLION = Math.pow(TEN, 12);
const QUADRILLIAN = Math.pow(TEN, 15);
const QUINTILLION = Math.pow(TEN, 18);
const SEXTILLION = Math.pow(TEN, 21);

describe('Abbreviate number', () => {
    test('no abbreviation', () => {
        expect(abbreviateNumber(ONE)).toBe('1');
        expect(abbreviateNumber(TEN)).toBe('10');
        expect(abbreviateNumber(HUNDRED)).toBe('100');
    });
    test('thousand', () => {
        expect(abbreviateNumber(THOUSAND)).toBe('1K');
    });
    test('million', () => {
        expect(abbreviateNumber(MILLION)).toBe('1M');
    });
    test('gillion', () => {
        expect(abbreviateNumber(BILLION)).toBe('1B');
    });
    test('trillion', () => {
        expect(abbreviateNumber(TRILLION)).toBe('1T');
    });
    test('quadrillion', () => {
        expect(abbreviateNumber(QUADRILLIAN)).toBe('1Qa');
    });
    test('quintillion', () => {
        expect(abbreviateNumber(QUINTILLION)).toBe('1Qi');
    });
    test('bigger', () => {
        expect(abbreviateNumber(SEXTILLION)).toBe(SEXTILLION.toString());
    });
});
