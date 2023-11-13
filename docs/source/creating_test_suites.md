# Creating test suites

## What data should I use?

It is best to use data that is as close to your production use case as possible. We recommend sampling some historic data and manually validating a set of 25+ cases.

Public datasets on HuggingFace like the [Dolly dataset](https://huggingface.co/datasets/databricks/databricks-dolly-15k) and the [HumanEval dataset](https://huggingface.co/datasets/openai_humaneval) can be a great starting place to benchmark on your use case before you have data that is closer to your actual production setting.

When no baseline examples or labels easily exist for the inputs you want to evaluate LLM performance on, you can use an existing LLM to generate a baseline for the task and then iterate from there.

## Ways to create a test suite

The `TestSuite` class is the main touch point for creating and running tests in Arthur Bench. No matter how you prepare your data for a test suite, you use the common interface provided by importing the `TestSuite` class:

```python
from arthur_bench.run.testsuite import TestSuite
```

You can provide data for your `TestSuite` via the following options, each of which we give examples of in the sections below:
1. `List[str]`
2. `pd.DataFrame`
3. CSV file
4. HuggingFace Dataset

To see the exact specifications for the `TestSuite` class, visit our [SDK docs](https://bench.readthedocs.io/en/latest/sdk/arthur_bench.run.html#arthur_bench.run.testsuite.TestSuite).

### `List[str]` -> `TestSuite`

You can create and run a test suite by passing lists of strings directly as the test suite data:

```python
suite = TestSuite(
    "bench_quickstart", 
    "exact_match",
    input_text_list=["What year was FDR elected?", "What is the opposite of down?"], 
    reference_output_list=["1932", "up"]
)
suite.run('quickstart_run', candidate_output_list=["1932", "up is the opposite of down"])
```

This path also allows you to pass LLM responses directly into a test suite as a set of baseline reference outputs and/or as a run of candidate outputs. For example, you can use `gpt-4` outputs as a baseline for a test suite, and then run `gpt-3.5-turbo` as a candidate to see how it compares.

Creating and running the test suite directly from LLM-generated strings:

```python
from langchain.chat_models import ChatOpenAI
gpt35 = ChatOpenAI()
gpt4 = ChatOpenAI(model_name="gpt-4")

inputs = ["What year was FDR elected?", "What is the opposite of down?"]
baseline_outputs = [gpt4.predict(x) for x in inputs]
candidate_outputs = [gpt35.predict(x) for x in inputs]

suite = TestSuite(
    "bench_llm_quickstart", 
    "exact_match",
    input_text_list=inputs, 
    reference_output_list=baseline_outputs
)
suite.run('quickstart_llm_run', candidate_output_list=candidate_outputs)
```

### `DataFrame` -> `TestSuite`

If you have your test suite and/or model response data in a pandas DataFrame you can create test suites and runs directly from those dataframes

Here is an example test suite built from a dataframe with the default reference data and candidate data column names that `TestSuite` expects (you can also use other column names as we show below)

Creating and running the default DataFrame test suite:

```python
import pandas as pd
df = pd.DataFrame({
    "input": ["What year was FDR elected?", "What is the opposite of down?"],
    "reference_output": ["1932", "up"],
    "candidate_output": ["1932", "up is the opposite of down"]
})

test_suite = TestSuite(
    "suite_from_df", 
    "exact_match", 
    reference_data=df
)

test_suite.run("candidate_from_df", candidate_data=df)
```

Alternatively you can create and run test suites from dataframes with custom column names.

Creating and running the custom DataFrame test suite:

```python
import pandas as pd
df = pd.DataFrame({
    "my_input": ["What year was FDR elected?", "What is the opposite of down?"],
    "baseline_output": ["1932", "up"],
    "gpt35_output": ["1932", "up is the opposite of down"]
})

test_suite = TestSuite(
    "suite_from_df_custom", 
    "exact_match", 
    reference_data=df,
    input_column="my_input",
    reference_column="baseline_output"
)

test_suite.run(
    "candidate_from_df_custom", 
    candidate_data=df, 
    candidate_column="gpt35_output"
)
```

### `.csv` -> `TestSuite`

If your test suite and/or model response data already exists in CSV files you can create test suites and runs directly from those files

Here is an example test suite CSV with the default reference data and candidate data column names that `TestSuite` expects (you can also use other column names as we show below)

`test_suite_data_default_columns.csv`
```csv
input, reference_output, candidate_output
What year was FDR elected?, 1932, 1932
What is the opposite of down?, up, up is the opposite of down
```

Creating and running the default csv test suite:

```python
test_suite = TestSuite(
    "suite_from_csv", 
    "exact_match", 
    reference_data_path="/path/to/test_suite_data_default_columns.csv"
)

test_suite.run(
    "candidate_from_csv", 
    candidate_data_path="/path/to/test_suite_data_default_columns.csv"
)
```

Alternatively you can create and run test suites from `.csv` files with custom column names:

`test_suite_data_custom_columns.csv`
```csv
my_input, baseline_output, gpt35_output
What year was FDR elected?, 1932, 1932
What is the opposite of down?, up, up is the opposite of down
```

Creating and running the custom csv test suite:

```python
test_suite = TestSuite(
    "suite_from_csv_custom", 
    "exact_match", 
    reference_data_path="/path/to/test_suite_data_custom_columns.csv",
    input_column="my_input",
    reference_column="baseline_output"
)

test_suite.run(
    "candidate_from_csv_custom", 
    candidate_data_path="/path/to/test_suite_data_custom_columns.csv",
    candidate_column="gpt35_output"
)
```

### HuggingFace dataset -> `DataFrame` -> `TestSuite`

Here we create a small question-answering test suite from the Dolly dataset downloaded from HuggingFace. We set up the test suite to use BERTScore to measure similarity between candidate answers and reference answers

Creating and running the dolly test suite:

```python

# get dolly dataset from huggingface into a pandas dataframe
import pandas as pd
from datasets import load_dataset
dolly = load_dataset("databricks/databricks-dolly-15k")
dolly_df = pd.DataFrame(dolly["train"])

# make test suite from a question-answering subset of the data
dolly_df_sample = dolly_df[dolly_df["category"]=="open_qa"].sample(25, random_state=278487)
dolly_suite = TestSuite(
    "suite_from_huggingface_dolly", 
    "bertscore", 
    reference_data=dolly_df_sample,
    input_column="instruction",
    reference_column="response"
)

# run test suite on gpt-3.5-turbo generated answers to the questions
from langchain.chat_models import ChatOpenAI
gpt35 = ChatOpenAI()
dolly_suite.run(
    "gpt-3.5", 
    candidate_output_list=[gpt35.predict(x) for x in dolly_df_sample.instruction])
```
