# Quickstart

Make sure you have completed installation from the [setup](setup.md) guide before moving on to this quickstart.

## (Optional) Environment Setup

Set the environment variable BENCH_FILE_DIR to point to the local directory where you want your test results to be saved (this will by default be "./bench_runs", a folder inside the directory wherever you are running your tests from). 

```
export BENCH_FILE_DIR="your/bench/file/dir/"
```

## Creating your first test suite

Instantiate a test suite with a name, data, and scorer.

This example creates a test suite from lists of strings directly with the `exact_match` scorer. 

```python
from arthur_bench.run.testsuite import TestSuite
suite = TestSuite(
    'bench_quickstart', 
    'exact_match',
    input_text_list=["What year was FDR elected?", "What is the opposite of down?"], 
    reference_output_list=["1932", "up"]
)
```

You can create test suites from a pandas DataFrame or from a path to a local CSV file. See the [test suite creation guide](creating_test_suites.md) to view all the ways you can create test suites.

You can view all scorers available out of the box with bench here on our [scoring](scoring.md) page, as well as [customize](custom_scoring.md) your own.

## Running your first test suite

To create a **Test Run**, you only need to specify the candidate responses. See the [test suite creation guide](creating_test_suites.md) to view all the ways you can run test suites.

```python
run = suite.run('quickstart_run', candidate_output_list=["1932", "up is the opposite of down"])
print(run)
```

```python
>>> [TestCaseOutput(output='1932', score=1.0), TestCaseOutput(output='up is the opposite of down', score=0.0)]
```

You should now have logged test case results with scores of 1.0 and 0.0, respectively.

## View results in local UI

Now run `bench` from the command line to launch the local UI and explore the test results.

```
bench
```

## Next Steps

Now that you have set up and ran your first test suite, check out the rest of the [scorers](scoring.md) available in Arthur Bench out of the box. 

To learn more about the basic concepts around data and testing in Arthur Bench, visit our [basic concepts guide](concepts.md).

