## Quickstart

Make sure you have completed installation from the [setup](setup.md) guide before moving on to this quickstart.

### Creating your first test suite

Instantiate a test suite with a name, data, and scoring method.

This example creates a test suite from lists of strings directly with the `exact_match` scoring method. 

```python
from arthur_bench.run.testsuite import TestSuite
suite = TestSuite(
    'bench_quickstart', 
    'exact_match'
    input_text_list=["What year was FDR elected?", "What is the opposite of down?"], 
    reference_output_list=["1932", "up"]
)
```

You can create test suites from a pandas DataFrame or from a path to a local CSV file. See the [test suite creation guide](creating_test_suites.md) to view all the ways you can create test suites.

You can view all scoring methods available out of the box with bench here on our [scoring](scoring.md) page, as well as [customize](custom_scoring.md) your own.

### Running your test suite

To create a **Test Run**, you only need to specify the candidate responses (as a a list of strings, a pandas DataFrame, or a path to a CSV file) and Bench will score the run:

```python
suite.run('quickstart_run', candidate_output_list=["1932", "up is the opposite of down"])
```

You should now have logged test case results with scores of 1.0 and 0.0, respectively.

### View results in local UI
Run `bench` from the command line to launch the local UI and explore the test results.

