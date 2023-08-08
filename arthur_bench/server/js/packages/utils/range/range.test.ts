import range from './index';

describe('range', () => {
    test('number range', () => {
        expect(range(4, 10, 1)).toEqual([4, 5, 6, 7, 8, 9, 10]);
    });
});
