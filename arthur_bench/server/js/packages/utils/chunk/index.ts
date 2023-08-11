export const chunkArray = (arr: Array<any>, chunkSize: number = 10) => {
    const chunkArray = [];
    for (let i = 0; i < arr.length; i += chunkSize) {
        const chunk = arr.slice(i, i + chunkSize);
        chunkArray.push(chunk);
    }

    return chunkArray;
};
