## Creating test suites

### What data should I use to create a test suite?

It is best to use data that is as close to your production use case as possible. If possible, we recommend sampling some historic data and manually validating a set of 25+ cases. If that is not possible, manually selecting some some inputs and using a foundation model to generate a starting set of reference outputs is a good option.

#### Public benchmarks & datasets

Public datasets on HuggingFace like the [Dolly dataset](https://huggingface.co/datasets/databricks/databricks-dolly-15k) and the [HumanEval dataset](https://huggingface.co/datasets/openai_humaneval) can be a great starting place to benchmark on your use case before you have data that is closer to your actual production setting.

#### LLM generations as baseline

When no baseline examples easily exist for the inputs you want to evaluate LLM performance on, you can use an existing LLM to generate a good enough set of baseline outputs for the task.

### Ways to create a test suite

No matter how you prepare your data for a test suite, you use the common interface provided by importing the `TestSuite` class:

```python
from arthur_bench.run.testsuite import TestSuite
```

#### strings -> test suite

**Toy example**

This simple quickstart example shows how to create and run a test suite by passing lists of strings

```python
suite = TestSuite(
    'bench_quickstart', 
    input_text_list=["What year was FDR elected?", "What is the opposite of down?"], 
    reference_output_list=["1932", "up"]
)
suite.run('quickstart_run', candidate_output_list=["1932", "up is the opposite of down"])
```

**LLM APIs**
This path also allows you to pass LLM responses directly into a test suite as a set of baseline reference outputs and/or as a run of candidate outputs. For example, you can use `gpt-4` outputs as a baseline for a test suite, and then run `gpt-3.5-turbo` as a candidate to see how it compares.

```python
from langchain.chat_models import ChatOpenAI
gpt35 = ChatOpenAI()
gpt4 = ChatOpenAI(model_name="gpt-4")

inputs = ["What year was FDR elected?", "What is the opposite of down?"]
baseline_outputs = [gpt4.predict(x) for x in inputs]
candidate_outputs = [gpt35.predict(x) for x in inputs]

suite = TestSuite(
    'bench_llm_quickstart', 
    input_text_list=inputs, 
    reference_output_list=baseline_outputs
)
suite.run('quickstart_llm_run', candidate_output_list=candidate_outputs)
```

#### DataFrame -> test suite

If you have your test suite and/or model response data in a pandas DataFrame you can create test suites and runs directly from those dataframes

**Default column names**

Here is an example test suite built from a dataframe with the default reference data and candidate data column names that `TestSuite` expects (you can also use other column names as we show below)

```python
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
```

Running test suite:

```python
test_suite.run("candidate_from_df", candidate_data=df)
```

**Custom column names**

```python
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
    reference_output="baseline_output"
)
```

Running test suite:

```python
test_suite.run(
    "candidate_from_df_custom", 
    candidate_data=df, 
    candidate_column="gpt35_output"
)
```

#### CSV -> test suite

If your test suite and/or model response data already exists in CSV files you can create test suites and runs directly from those files

**Default column names**

Here is an example test suite CSV with the default reference data and candidate data column names that `TestSuite` expects (you can also use other column names as we show below)

`test_suite_data_default_columns.csv`
```csv
input, reference_output, candidate_output
What year was FDR elected?, 1932, 1932
What is the opposite of down?, up, up is the opposite of down
```

Creating test suite:

```python

test_suite = TestSuite(
    "suite_from_csv", 
    "exact_match", 
    reference_data_path="/path/to/test_suite_data_default_columns.csv"
)
```

Running test suite:

```python
test_suite.run(
    "candidate_from_csv", 
    candidate_data_path="/path/to/test_suite_data_default_columns.csv"
```

**Custom column names**

`test_suite_data_custom_columns.csv`
```csv
my_input, baseline_output, gpt35_output
What year was FDR elected?, 1932, 1932
What is the opposite of down?, up, up is the opposite of down
```

Creating test suite:

```python

test_suite = TestSuite(
    "suite_from_csv_custom", 
    "exact_match", 
    reference_data_path="/path/to/test_suite_data_custom__columns.csv",
    input_column="my_input",
    reference_column="baseline_output"
)
```

Running test suite:

```python
test_suite.run(
    "candidate_from_csv_custom", 
    candidate_data_path="/path/to/test_suite_data_custom_columns.csv",
    candidate_column="gpt35_output"
```

#### HuggingFace dataset -> DataFrame -> test suite

Here we create a small question-answering test suite from the Dolly dataset downloaded from HuggingFace. We set up the test suite to use BERTScore to measure similarity between candidate answers and reference answers

Creating test suite:

```python
import pandas as pd
from datasets import load_dataset
dolly = load_dataset("databricks/databricks-dolly-15k")
dolly_df = pd.DataFrame(dolly["train"])
dolly_df_sample = dolly_df[dolly_df["category"]=="open_qa"].sample(25, random_state=278487)

dolly_suite = TestSuite(
    "suite_from_huggingface_dolly", 
    "bertscore", 
    reference_data=dolly_df_sample,
    input_column="instruction",
    reference_output="response"
)
```

Running test suite:

```python
from langchain.chat_models import ChatOpenAI
gpt35 = ChatOpenAI()
dolly_suite.run(
    "gpt-3.5", 
    candidate_output_list=[gpt35.predict(x) for x in dolly_df_sample.instruction])
```