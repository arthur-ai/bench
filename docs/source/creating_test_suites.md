## Creating test suites

### What data should I use to create a test suite?

It is best to use data that is as close to your production use case as possible. If possible, we recommend sampling some historic data and manually validating a set of 25+ cases. If that is not possible, manually selecting some some inputs and using a foundation model to generate a starting set of reference outputs is a good option.

#### Public benchmarks & datasets

Public datasets on HuggingFace like the [Dolly dataset](https://huggingface.co/datasets/databricks/databricks-dolly-15k) and the [HumanEval dataset](https://huggingface.co/datasets/openai_humaneval) can be a great starting place to benchmark on your use case before you have data that is closer to your actual production setting.

#### LLM generations as baseline

When no baseline examples easily exist for the inputs you want to evaluate LLM performance on, you can use an existing LLM to generate a good enough set of baseline outputs for the task.

For example, for our summarization test suite, we were able to generate a good enough baseline using we (TODO LINK)

### Paths to create a test suite

#### strings in memory -> test suite

This simple quickstart example shows how to create and run a test suite by passing lists of strings

```python
suite = TestSuite(
    'bench_quickstart', 
    input_text_list=["What year was FDR elected?", "What is the opposite of down?"], 
    reference_output_list=["1932", "up"]
)
suite.run('quickstart_run', candidate_output_list=["1932", "up is the opposite of down"])
```

This path also allows you to test LLM responses from an API and then pass the responses into a test suite as a set of baseline reference outputs and/or as a run of candidate outputs. For example, you can use `gpt-4` outputs as a baseline for a test suite, and then run `gpt-3.5-turbo` as a candidate to see how it compares.

```python
import openai
def openai_response(input_text, model):
    return openai.ChatCompletion.create(
        model=model, 
        max_tokens=30,
        messages=[
            {"role" : "system", "content" : "You are a helpful assistant."},
            {"role" : "user", "content" : input_text}
        ])['choices'][0]['message']['content']

inputs = ["What year was FDR elected?", "What is the opposite of down?"]
baseline_outputs = [openai_response(x, "gpt-4") for x in inputs]
suite = TestSuite(
    'bench_llm_quickstart', 
    input_text_list=inputs, 
    reference_output_list=baseline_outputs
)

candidate_outputs = [openai_response(x, "gpt-3.5-turbo") for x in inputs]
suite.run('quickstart_llm_run', candidate_output_list=candidate_outputs)
```

#### dataframe (with / without column names) -> test suite

#### local csv (with / without column names) -> test suite

#### HuggingFace load_dataset -> dataframe & column names -> test suite

Here is how you can create a test suite from the HumanEval dataset downloaded from huggingface

```python
humaneval_code_dataset = load_dataset("openai_humaneval")
humaneval_df = pd.DataFrame(humaneval_code_dataset["test"])

unit_tests = [
    f'\n{humaneval_df.loc[i]["test"]}\ncheck({humaneval_df.loc[i]["entry_point"]})' 
    for i in range(len(humaneval_df))
]
python_scorer = PythonUnitTesting(unit_tests=unit_tests)
python_suite = TestSuite(
    "humaneval", 
    python_scorer, 
    reference_data=humaneval_df,
    input_column="prompt",
    reference_output="canonical_solution"
)
```

For an explanation of the unit test construction here, see our [code evaluation guide](code_evaluation.md)
