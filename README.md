# Bench

Bench is built for evaluating LLMs for production use cases. Bench can be used for comparing any two sets of generated responses to a set of inputs. Some things you might want to compare include:
- Different prompt versions
- Different foundation models or language model providers
- Different open source models
- Different generation hyperparameters

## Getting started

### Package installation and environment setup
First download the tar file from the Github releases. Next install the package to your python environment.

Install Bench with optional dependencies for serving results locally (recommended):  
`pip install --find-links=./directory_with_tar_file 'arthur-bench[server]'`

Install Bench with minimum dependencies:
`pip install --find-links=./directory_with_tar_file 'arthur-bench'`

Bench saves test suites and test runs to the directory specified by the `BENCH_FILE_DIR`, which defaults to `./bench`

#### Exploring the UI with Examples
The following commands will spin up a local UI serving two example test suites we've added

```
git clone git@github.com:arthur-ai/bench.git
cd bench/examples  # navigate to bench root directory
bench
```
This will spin up a server where you can view sample created Test Suites and evaluate Runs across different model and prompt configurations.

In the `examples/` folder, you will find demo notebooks used to generate the Test Suites and Run results recorded in the directory. 
**To run these notebooks directly, configure the BENCH_FILE_DIR to a new file system in the top cell of the notebook.** Please use these as a a reference in creating your own Test Suites and Runs.

## Key Concepts

### DATA
<p align="center">
<img src="./docs/source/_static/img/Reference_df.png" alt="Reference_df" width="750"/>

Using Bench requires data, including information such as:

**A Reference Dataset:**
- **Inputs** to the LLM. For *Summarization* tasks, this may be the document to be summarized. For *Question & Answering* tasks, this may be the question asked.
- **Reference Outputs**: these are your baseline outputs. Teams can use either human-labeled ground truth annotations or the outputs from your LLM model in production that you are using Bench to compare against.

**A Candidate Dataset**
- **Candidate Outputs**: these are the outputs from your new candidate LLM.
- **Context**: contextual information for Question & Answering tasks.

[//]: # (TODO: are the latter  two part of the reference dataset?)

#### An Example

Consider the task of *Question & Answering* about specific documents: 

> **Reference Dataset:**
> - **Input**: "What war was referred to in the Gettysburg Address?"
> - **Reference Output**: The American Civil War
> 
> **Candidate Dataset:**
> - **Candidate Output**: The American War
> - **Context**: _(The Gettysburg Address)_ "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal ...
> that this nation, under God, shall have a new birth of freedom – and that government of the people, by the people, for the people, shall not perish from the earth."

### TESTING STRUCTURE
 
 <p align="center">
<img src="./docs/source/_static/img/test_suite_run.png" alt="test_suites_runs" width="750"/>

#### Test Suites

A **Test Suite** can hold Input data and Reference Outputs as well as a _Scoring Method_ which will be used to compare the reference outputs to the candidate outputs provided in each **Test Run**. 

For example, for a summarization task, your **Test Suite** might include the documents to summarize, desirable reference summaries, and the [summary quality](#summary_quality) scoring metric.

Reference data can be provided via CSV file, a pandas DataFrame, or lists of strings for inputs and reference outputs. Please see our [documentation](https://docs.arthur.ai/bench/index.html) for more detail. To create a test suite in Bench:



```
from arthur_bench.run.testsuite import TestSuite

suite = TestSuite('my_bench_test', reference_data_path='./path/to/my_data.csv', scoring_method='bertscore')
```

#### Test Runs

A **Test Run** contains a set of Candidate Outputs and optional Context, and can additionally specify metadata which indicates how the candidate outputs were generated. For example, on the document summarization task, we might want to create a run to assess the responses of gpt 3.5, using prompt version `my_custom_prompt`.

To create a **Test Run**, you only need to specify the candidate responses (as a CSV file, a pandas DataFrame, or a list of strings) and Bench will score the run:

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

## Scoring Methods

A **Scoring Method** is the criteria used to judge the candidate outputs for each run of the test suite. Each {class}`scoring method <arthur_bench.scoring.scoring_method.ScoringMethod>` implements the `run_batch` method to compute a score for a model output. Bench includes both embedding based methods like bert score as well as LLM-guided evaluations.

| Scoring Method                    | Tasks | Requirements |
|-----------------------------------|-----|-----|
| Exact Match (`exact_match`) | any| Reference Output, Candidate Output|
| BERT Score (`bertscore`)          | any | Reference Output, Candidate Output|
| Summary Quality (`summary_quality`)  | Summarization | Input, Reference Output, Candidate Output|
| QA Correctness (`qa_correctness`) | Question-Answering| Input, Candidate Output, Context|

#### `exact_match`

The ExactMatch metric evaluates, for each test case, whether the candidate LLM output is an exact match of the provided reference output.

#### `bertscore`

[BERTScore](https://arxiv.org/abs/1904.09675) is a quantitative metric to compare the similarity of two pieces of text. Using the `bertscore` scoring method will score each row of the test run as the bert score between the reference output and the candidate output.

#### `summary_quality`

The Summary Quality scoring method is a comprehensive measure of summarization quality compared to a reference. It evaluates summaries on dimensions including relevance and syntax. Each row of the test run will receive a binary 0, indicating that the reference output was scored higher than the candidate output, or 1, indicating that the candidate output was scored higher than the reference output.

#### `qa_correctness`

The QA correctness metric evaluates the correctness of an answer, given a question and context. This scoring method does not require a reference output, but does require context. Each row of the Test Run will receive a binary 0, indicating an incorrect output, or 1, indicating a correct output.

#### `code_eval`

The CodeEval metric evaluates whether the provided candidate output (an LLM-generated script) passes the unit test provided in the reference output. This scoring method wraps the [`code_eval`](https://huggingface.co/spaces/evaluate-metric/code_eval) metric interface from HuggingFace 

## FAQ

### What can I do with Bench?

Bench can be used for comparing any two sets of generated responses to a set of inputs. Some things you might want to try:
- Different prompt versions
- Different foundation models or language model providers
- Different open source models
- Different generation hyperparameters

See the examples directory for some examples of creating test suites and runs for some of these model parameters.

### What data should I use for my test suite?

It is best to use data that is as close to your production use case as possible. If possible, we recommend sampling some historic data and manually validating a set of 25+ cases. If that is not possible, manually selecting some some inputs and using a foundation model to generate a starting set of reference outputs is a good option.
