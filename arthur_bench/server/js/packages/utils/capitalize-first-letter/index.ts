/**
 *
 * @param word A string
 * @returns Original string with first character capitalized
 */
export function capitalizeFirstLetter(word: string) {
    if (word) {
        const firstChar = word.charAt(0).toUpperCase();
        if (word.length > 1) {
            return firstChar + word.slice(1);
        }
        return firstChar;
    }
    return word;
}
