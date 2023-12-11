import { TTestRunData } from "arthur-redux/slices/testSuites/types";

const formatTestRunData = (data: TTestRunData[]) => {
    const formattedData = [];

    for (let i = 0; i < data.length; i++) {
        const testRun = data[i];
        const testCases = testRun.test_case_runs;

        for (let j = 0; j < testCases.length; j++) {
            const testCase = testCases[j];
            const test_case_id = testCase.id;
            const reference_output = testCase.reference_output;
            const input = testCase.input;
            const output = testCase.output;
            const score = testCase.score;
            const outputs = [];

            for (let k = 0; k < data.length; k++) {
                const testRun = data[k];
                const testRunId = testRun.id;
                const testRunName = testRun.name;
                outputs.push({
                    id: testRunId,
                    name: testRunName,
                    output,
                    score,
                });
            }
            formattedData.push({
                test_case_id,
                reference_output,
                input,
                outputs,
            });
        }
    }

    return formattedData;
};

export default formatTestRunData;
