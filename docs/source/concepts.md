### Key Concepts
 
<p align="center">
<img src="./_static/img/test_suite_run.png" alt="test_suites_runs" width="750"/>

#### Test Suites

A **Test Suite** can hold Input data and Reference Outputs as well as a _Scoring Method_ which will be used to compare the reference outputs to the candidate outputs provided in each **Test Run**. 

For example, for a summarization task, your {class}`Test Suite <arthur_bench.run.testsuite.TestSuite>` might include the documents to summarize, desirable reference summaries, and the {class}`Summary Quality <arthur_bench.scoring.summary_quality.SummaryQuality>` scoring metric.

Reference data can be provided via csv file, a pandas dataframe, or lists of strings for inputs and reference outputs. To create a test suite in Bench:

```
from arthur_bench.run.testsuite import TestSuite

suite = TestSuite('my_bench_test', reference_data_path='./path/to/my_data.csv', scoring_method='bertscore')
```

#### Test Runs

A **Test Run** contains a set of Candidate Outputs and optional Context, and can additionally specify metadata which indicates how the candidate outputs were generated. For example, on the document summarization task, we might want to create a run to assess the responses of gpt 3.5, using prompt version `my_custom_prompt`.

To create a {class}`Test Run <arthur_bench.run.testrun.TestRun>`, you only need to specify the candidate responses (as a csv file, a pandas dataframe, or a list of strings) and Bench will score the run:

```
suite.run('my_bench_run', candidate_data_path='./path/to/my_model_data.csv', model_name='openai_gpt_35', foundation_model='gpt-3.5-turbo', prompt_template='my_custom_prompt')

```

#### Scoring Methods

A **Scoring Method** is the criteria used to judge the candidate outputs for each run of the test suite. Each {class}`scoring method <arthur_bench.scoring.scoring_method.ScoringMethod>` implements the `run_batch` method to compute a score for a model output. Bench includes both embedding based methods like bert score as well as LLM-guided evaluations.