import { Output, TTestRunData } from "arthur-redux/slices/testSuites/types";

/**
 * Formats test run data into a specific structure for the compare test runs table.
 *
 * @param {TTestRunData[]} data - The test run data to be formatted.
 * @returns {Array} The formatted data.
 */
const formatTestRunData = (data: TTestRunData[]) => {
    if (!data || !data.length) return [];
    const formattedData = [];

    const firstRow = data[0];
    const testCases = firstRow.test_case_runs;

    for (let i = 0; i < testCases.length; i++) {
        const testCase = testCases[i];
        const formattedRow = {
            testCaseId: testCase.id,
            input: testCase.input,
            referenceOutput: testCase.reference_output,
            outputs: [] as Output[],
        };

        for (let j = 0; j < data.length; j++) {
            const testRun = data[j];
            const testCaseRun = testRun.test_case_runs[i];
            const output = {
                id: testRun.id,
                name: testRun.name,
                output: testCaseRun.output,
                score: testCaseRun.score,
            };
            formattedRow.outputs.push(output);
        }

        formattedData.push(formattedRow);
    }
    return formattedData;
};

export default formatTestRunData;
