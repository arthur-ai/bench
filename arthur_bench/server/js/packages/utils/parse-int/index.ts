/**
 * An integer parsing utility. Rounds floats to the nearest integer
 *
 * @param x A value to parse
 * @param base Number base for conversion. Defaults to base 10
 * @returns A number or null
 */
export function parseInt(x: string | number, base = 10) {
    if (typeof x === 'string') {
        const parsed = Number.parseInt(x, base);
        if (Number.isNaN(parsed)) {
            return null;
        }
        return Math.round(parsed);
    }

    if (typeof x === 'number' || typeof x === 'bigint') {
        return Math.round(x);
    }

    return null;
}
