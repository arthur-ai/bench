# Code Evaluation

## Basic Usage

Code evaluation refers to the process of checking whether LLM-written code passes unit tests

To use a code evaluation scoring method, instantiate the scorer with the unit tests you want to attach to the suite, and proceed with test suite creation / test case running as usual. 

Here we show the basic usage for the PythonUnitTesting code evaluation scorer. See the Data Requirements and Example Walkthrough sections below for more details on preparing unit tests and candidate solutions.

```python
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import PythonUnitTesting

# create scorer from unit_tests: List[str]
python_scorer = PythonUnitTesting(unit_tests=unit_tests)

# create test suite
# we explain how to prepare the data for python_unit_test_df below
python_suite = TestSuite(
    "python_testsuite", 
    python_scorer,
    reference_data=python_unit_test_df 
)
```

## Data Requirements

### Unit tests

Unit tests must be compatible with the `code_eval` evaluator metric from [HuggingFace](https://huggingface.co/spaces/evaluate-metric/code_eval), which is what the `PythonUnitTesting` scoring method uses under the hood.

**Format**

Each unit test is expected to invoke the candidate function by name and assert its output

The general format of the unit test expected by bench is as follows (the name `check` is not required)

```python
def check(candidate):
    assert candidate(test_input_0) = test_output_0
    assert candidate(test_input_1) = test_output_1
    assert candidate(test_input_2) = test_output_2
    # ...
check(candidate_function_name)
```

**Provide unit tests as strings**

Unit tests can be passed to the `PythonUnitTesting` scorer as a list of strings, which is likely the simpler option if you are loading tests from a benchmark dataset (e.g. `HumanEval` as we do in the example below):

```python
# create scorer from unit_test: List[str]
python_scorer = PythonUnitTesting(unit_tests=unit_tests)
```

**Provide unit tests as directory**

Alternatively you can load unit tests from a directory to evaluate your candidate solutions. Given a directory of unit test scripts:

```
unit_test_dir_name:
- unit_test_0.py
- unit_test_1.py
...
```

The `PythonUnitTesting` scorer can be created just from that directory name:

```python
python_scorer = PythonUnitTesting(unit_test_dir=unit_test_dir_name)
```

### Solutions

Candidate solutions will only be evaluated to be correct if they contain:

- a function to call (in the HumanEval dataset, this is called the `entry_point`)
- any necessary imports

This is correct:

```python
import math

def greatest_common_divisor(a: int, b: int) -> int:
    return math.gcd(a, b)
```

This will be scored as incorrect due to missing the `math` import

```python
def greatest_common_divisor(a: int, b: int) -> int:
    return math.gcd(a, b)
```

This will be scored as incorrect due to missing a function entrypoint for the unit test to invoke:

```python
import math

return math.gcd(a, b)
```

### Input prompts & reference outputs

Input prompts and reference outputs (AKA canonical / golden solutions) have **no requirements** in Bench. These components are only for your own analysis, and are not used by the scoring methods under the hood in code evaluation.

## Example Walkthrough

Here is some example code that you can use to generate and compare python coding solutions using OpenAI's GPT-3.5 and Anthropic's Claude-2 on the [HumanEval dataset](https://huggingface.co/datasets/openai_humaneval) from HuggingFace

**Environment variables**

First we set environment variables for `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` before running our generation code
```
export "OPENAI_API_KEY"="sk-..."
export "ANTHROPIC_API_KEY"="sk-ant-..."
```

**Load HumanEval data**

Our dataset is the HumanEval dataset from HuggingFace loaded into a pandas DataFrame

```python
from datasets import load_dataset
import pandas as pd

humaneval_code_dataset = load_dataset("openai_humaneval")
humaneval_df = pd.DataFrame(humaneval_code_dataset["test"])
```

**Prepare unit tests**

We prepare the unit tests to invoke each candidate function using the `test` and `entry_point` fields of the HumanEval dataset:

```python
unit_tests = [
    f'\n{humaneval_df.loc[i]["test"]}\ncheck({humaneval_df.loc[i]["entry_point"]})' 
    for i in range(len(humaneval_df))
]
```

To view an example, here is the unit test for the `greatest_common_divisor` task:

```python
def check(candidate):
    assert candidate(3, 7) == 1
    assert candidate(10, 15) == 5
    assert candidate(49, 14) == 7
    assert candidate(144, 60) == 12

check(greatest_common_divisor)
```

**Generate solutions**

```python
from langchain.chat_models import ChatOpenAI, ChatAnthropic
gpt35 = ChatOpenAI()
claude = ChatAnthropic()

prompt_template = """
You are a bot that gives answers to coding tasks only. If the task is a coding task, give an expert python solution.
If the task is unrelated, give the response "I don't know."
ALWAYS mark the beginning and end of your solution with ```python markdown markers.
Without these markers, the code cannot be extracted. Therefore the markers are required.
===
<text>
===
Solution:
"""

# used to extract the portion of an LLM response which is python code
extract_python = lambda x : x.replace('python\n', '').replace('```', '').replace(' def', 'def')

def get_solutions(model):
    filled_prompt_templates = [
        prompt_template.replace("<text>", humaneval_df[i]['prompt'])
        for i in range(len(humaneval_df))
    ]
    return [extract_python(model.predict(x)) for x in filled_prompt_templates]

gpt35_solutions = get_solutions(gpt35)
claude_solutions = get_solutions(claude)
```

**Create and run test suite**

Now that you have generated solutions for each model, we can create a test suite and a run for each LLM

```python
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import PythonUnitTesting

python_scorer = PythonUnitTesting(unit_tests=unit_tests)

python_suite = TestSuite(
    "humaneval_testsuite", 
    python_scorer,
    input_text_list=list(humaneval.prompt.values),
    reference_output_list=list(humaneval_df.canonical_solution.values),
)

python_suite.run("gpt-3.5-turbo", candidate_output_list=gpt35_solutions)
python_suite.run("claude-2", candidate_output_list=claude_solutions)
```

### Best practices

#### Prompt Templating

Evaluation becomes more straightforward if you can easily extract the part of an LLM response which is its actual code solution. The simplest way to do that seems to be including an instruction in your prompt or system message that specifies to place code in between python markers in markdown, like this:

```python
<your code here>
```

We demonstrate an example of using this marker in the prompt template in the example above

#### Task description

Performance tends to improve on coding when your task description contains an explicit function signature that you want the solution to adhere to, as well as including example input/output behavior in its docstring.

As an example, here is the input prompt for the `greatest_common_divisor` coding task from HumanEval:

```python
def greatest_common_divisor(a: int, b: int) -> int:
    """ Return a greatest common divisor of two integers a and b
    >>> greatest_common_divisor(3, 5)
    1
    >>> greatest_common_divisor(25, 15)
    5
    """
```

Note that the HumanEval dataset prompts all contain docstrings like this one
