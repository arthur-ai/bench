const { isNil } = require('./index')

describe('Is Null or Undefined', () => {
    test('Check Undefined', () => {
        expect(isNil(undefined)).toBe(true)
    })

    test('Check Null', () => {
        expect(isNil(null)).toBe(true)
    })

    test('Check Zero number', () => {
        expect(isNil(0)).toBe(false)
    })

    test('Check positive number', () => {
        expect(isNil(2)).toBe(false)
    })

    test('Check empty string', () => {
        expect(isNil('')).toBe(false)
    })

    test('Check random string', () => {
        expect(isNil('random')).toBe(false)
    })
});
