# Add Scorer Configurations

In the quickstart, we showed how to use the `exact_match` scorer. By default, the `exact_match` scorer is case sensitive. This means, the scorer returns the value of `1` only when the candidate output matches the content and the capitalization of the reference output. 

If we want to ignore capitalization differences, we can add a configuration to the `exact_match` scorer.

## Creating the test suite

Instantiate a test suite with a name, scorer, input text, and reference outputs. For our use case, instead of invoking the scorer using the string representation (which corresponds to the default config), we will explicitly call the scorer and add optional configurations. 

```python
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import ExactMatch

suite = TestSuite(
    name='bench_quickstart', 
    scoring_method=ExactMatch(case_sensitive=False),
    input_text_list=["What year was FDR elected?", "What is the opposite of down?"], 
    reference_output_list=["1932", "up"]
)
```

## Running the test

To create a test run, we need to specify the candidate responses.

```python
run = suite.run('quickstart_run', candidate_output_list=["1932", "Up"])
print(run.test_cases)
```

```python
>>> [TestCaseOutput(output='1932', score=1.0), TestCaseOutput(output='Up', score=1.0)] 
```

We have now logged the results for both test cases as `1.0` even though the capitalization doesn't match the reference. This is non-default behavior for which we needed to configure the scorer while creating the test suite.


