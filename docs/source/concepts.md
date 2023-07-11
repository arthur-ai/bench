## Key Concepts
### Data
<!-- ![ref_df](img/Reference_df.png) -->
<p align="center">
<img src="./_static/img/Reference_df.png" alt="Reference_df" width="750"/>

Using Bench requires a reference dataset, including information such as:
- **Inputs** to the LLM. For *Summarization* tasks, this may be the document to be summarized. For *Question & Answering* tasks, this may be the question asked.
- **Reference Outputs**: these are your baseline outputs. Teams can use either human-labeled ground truth annotations or the outputs from your LLM model in production that you are using Bench to compare against.
- **Candidate Outputs**: these are the outputs from your new candidate LLM.
- **Context**: contextual information for Question & Answering tasks.

[//]: # (TODO: are the latter  two part of the reference dataset?)

#### An Example

Consider the task of *Question & Answering* about specific documents: 

 - **Input**: "What war was referred to in the Gettysburg Address?"
 - **Reference Output**: The American Civil War
 - **Candidate Output**: The American War
 - **Context**: _(The Gettysburg Address)_ "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal ... that this nation, under God, shall have a new birth of freedom – and that government of the people, by the people, for the people, shall not perish from the earth."

### Testing Structure
 
 
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

### Viewing your runs

Running `bench` from the command line will spin up a local server where you can view your test suites, runs, and scores.
This will require bench optional server dependencies to be installed.

### Running an existing test suite
Saved test suites can be loaded for reuse by name, without needing to specify data again. 

```
my_existing_suite = TestSuite('my_bench_test', 'bertscore')
```

### Scoring Methods

A **Scoring Method** is the criteria used to judge the candidate outputs for each run of the test suite. Each {class}`scoring method <arthur_bench.scoring.scoring_method.ScoringMethod>` implements the `run_batch` method to compute a score for a model output. Bench includes both embedding based methods like bert score as well as LLM-guided evaluations.

| Scoring Method                    | Tasks | Requirements |
|-----------------------------------|-----|-----|
| BERT Score (`bertscore`)          | any | Reference Output, Candidate Output|
| Summary Quality (`summary_quality`)  | Summarization | Input, Reference Output, Candidate Output|
| QA Correctness (`qa_correctness`) | Question-Answering| Input, Candidate Output, Context|

#### `bertscore`

[BERTScore](https://arxiv.org/abs/1904.09675) is a quantitative metric to compare the similarity of two pieces of text. Using the `bertscore` scoring method will score each row of the test run as the bert score between the reference output and the candidate output.

#### `summary_quality`

The Summary Quality scoring method is a comprehensive measure of summarization quality compared to a reference. It evaluates summaries on dimensions including relevance and syntax. Each row of the test run will receive a binary 0, indicating that the reference output was scored higher than the candidate output, or 1, indicating that the candidate output was scored higher than the reference output.

#### `qa_correctness`

The QA correctness metric evaluates the correctness of an answer, given a question and context. This scoring method does not require a reference output, but does require context. Each row of the Test Run will receive a binary 0, indicating an incorrect output, or 1, indicating a correct output.