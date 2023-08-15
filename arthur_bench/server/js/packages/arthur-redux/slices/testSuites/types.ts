export type TTestSuite = {
    id: string;
    name: string;
    scoring_method: TScoringMethod;
    last_run_time: string;
    updated_at: string;
    created_at: string;
};

export type TestSuiteCase = {
    id: string;
    input: string;
    reference_output: string;
};

export type TRunData = {
    runs: Run[] | null;
    pagination: TPagination
}

export type TTestSuiteData = {
    data: DetailedTestSuite | null;
    pagination: TPagination;
}

export type Run = {
    id: string;
    name: string;
    timestamp: string;
    model_name: string;
    model_version: string;
    foundation_model: string;
    prompt_template: string;
    avg_score: number;
    updated_at: string
};

export type DetailedTestSuite = {
    id: string;
    description: string;
    name: string;
    scoring_method: TScoringMethod;
    last_run_time: string;
    num_runs: number;
    test_cases: TestSuiteCase[];
};

export type TDistribution = {
    count: number;
    low: number;
    high: number;
}

export type TestRunSummary = {
    avg_score: number;
    name: string;
    histogram: TDistribution[];
    id: string
}
export type TSummary = {
    summaries: TestRunSummary[] | null;
    num_test_cases: number;
}

export type TPagination = {
    page: number;
    page_size: number;
    total_count: number;
    total_pages: number;
}

export type TestSuiteData = {
    data: TTestSuiteData | null;
    runs: TRunData | null;
    summaries: TSummary;
};

export type TestRunCase = {
    id: string;
    input: string;
    output: string;
    reference_output: string;
    score: number;
};

export type TTestRun = {
    data: TTestRunData | null;
    pagination: TPagination;
}

export type TTestRunData = {
    test_suite_id: string;
    test_case_runs: TestRunCase[];
    name: string;
    created_at: string,
    id: string
};

export type TTestSuitesState = {
    data: TTestSuite[] | null;
    currentTestSuite: TestSuiteData;
    currentTestRun: TTestRun;
    pagination: TPagination;
};

export type TScoringMethod = {
    name: EMethodType;
    type: string
}

export enum EMethodType {
    BERT = 'bertscore',
    SUMMARY = 'summary_quality',
    QA = 'qa_correctness',
}
