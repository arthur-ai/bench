/**
 *  Abbreviate a large number with a character suffix
 *  e.g. 10,000,000 -> 10M
 *
 * @param number can be an any integer
 * @return A string, representing an abbreviated number or original if too large
 */
export const abbreviateNumber = (number: number) => {
    const suffixes = ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi'];
    const suffix_index = (Math.log10(Math.abs(number)) / 3) | 0;
    const suffix = suffixes[suffix_index];

    if (typeof suffix === 'undefined') {
        return number.toString();
    }

    const scale = Math.pow(10, suffix_index * 3);
    const scaledNumber = number / scale;
    return scaledNumber.toFixed(0) + suffix;
};
