# Concepts
## Data
<!-- ![ref_df](img/Reference_df.png) -->
<p align="center">
<img src="./_static/img/Reference_df.png" alt="Reference_df" width="750"/>

Testing LLMs involves preparing the following data for your use case:
- **Inputs** to the LLM. Depending on the task at hand, these inputs are likely formatted to follow a **prompt template**.
- **Reference Outputs**: these are your baseline outputs. This would likely be either a ground truth response to the input, or the outputs from a baseline that you are evaluating against.
- **Candidate Outputs**: these are the outputs from your candidate LLM that you are scoring.
- **Context**: contextual information used to produce the candidate output, e.g. for retrieval-augmented Question & Answering tasks.

As an example, consider the task of *Question & Answering* about specific documents: 

 - **Input**: "What war was referred to in the Gettysburg Address?"
 - **Reference Output**: American Civil War
 - **Candidate Output**: The war referenced in the Gettysburg Address is the American Civil War
 - **Context**: _(Wikipedia)_ "The Gettysburg Address is a speech that U.S. President Abraham Lincoln delivered during the American Civil War at the dedication of the Soldiers' National Cemetery, now known as Gettysburg National Cemetery, in Gettysburg, Pennsylvania on the afternoon of November 19, 1863, four and a half months after the Union armies defeated Confederate forces in the Battle of Gettysburg, the Civil War's deadliest battle."

## Testing
 
<p align="center">
<img src="./_static/img/test_suite_run.png" alt="test_suites_runs" width="750"/>

### Test Suites

A **Test Suite** stores the input & reference output data along with a [scorer](scoring.md).

For example, for a summarization evaluation task, your test suite could be created with:

1. the documents to summarize
2. baseline summaries as reference outputs to evaluate against
3. the [SummaryQuality](https://bench.readthedocs.io/en/latest/scoring.html#summary-quality) scorer

To view how to create test suites from various data formats, view our [creating test suites guide](creating_test_suites.md)

### Test runs

When a test suite is run, its `scorer` is used to perform evaluation consistently across the candidate outputs provided in the run. 

To run your test suite on candidate data, pass the data to the `run()` function of your test suite, along with any additional metadata you want to be logged for that run. To view the metadata you can save with your test runs, see the [SDK docs](https://bench.readthedocs.io/en/latest/testsuite.html#arthur_bench.run.testrun.TestRun)

To view how to create test runs from various data formats, visit our [test suites guide](creating_test_suites.md)
