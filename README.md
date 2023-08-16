# Bench

Bench is a tool for evaluating LLMs for production use cases. Whether you are comparing different LLMs, considering different prompts, or testing generation hyperparameters like temperature and # tokens, Bench provides one touch point for all your LLM performance evalaution.

If you want:

- to know whether open source models can do as well as the top closed-source LLM API providers on your data
- to translate the rankings on existing LLM leaderboards into scores that you care about for your actual use case
- to standardize your workflow of LLM evaluation with a common interface across tasks and use cases

, then Bench can help with your LLM evaluation needs.

## Getting started

### Package installation and environment setup
First [download](https://github.com/arthur-ai/bench/releases) the tar file from the Github releases. Next install the package to your python environment.

Install Bench with optional dependencies for serving results locally (recommended):  
`pip install --find-links=./directory_with_tar_file 'arthur-bench[server]'`

Install Bench with minimum dependencies:
`pip install --find-links=./directory_with_tar_file 'arthur-bench'`

For further setup instructions visit our [installation guide](https://docs.arthur.com/bench/setup/index.html)


### Hello Bench

For a more in depth walkthrough of the following example, visit our [quickstart guide](https://docs.arthur.com/bench/quickstart.html)

Create a demo test suite and run the `exact_match` scoring method:

```python
from arthur_bench.run.testsuite import TestSuite
suite = TestSuite(
    'bench_quickstart', 
    input_text_list=["What year was FDR elected?", "What is the opposite of down?"], 
    reference_output_list=["1932", "up"]
)
suite.run('quickstart_run', candidate_output_list=["1932", "up is the opposite of down"])
```

To view the results in the local UI, run the simple command:

```
bench
```

This will require bench optional server dependencies to be installed.

### Running an existing test suite
Saved test suites can be loaded for reuse by name, without needing to specify data again. 

```
my_existing_suite = TestSuite('my_bench_test', 'bertscore')
```
