## Code Evaluation

### Basic Usage

Code evaluation refers to the process of checking whether LLM-written code passes unit tests

To do evaluation of coding tasks in Bench, you need the following components:

1. input prompt for each coding task
2. unit test for each coding task
3. LLM-written solution for each coding task

To use a code evaluation scoring method, instantiate the scorer with the unit tests you want to attach to the suite, and proceed with test suite creation / test case running as usual.

```python
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import PythonUnitTesting

# create scorer from unit_tests: List[str]
python_scorer = PythonUnitTesting(unit_tests=unit_tests)

# create test suite
python_suite = TestSuite(
    "humaneval_testsuite", 
    python_scorer,
    ...
)
```

See the section below the format and requirements of each of the components in more detail

### Requirements

#### Input prompts & reference outputs

Input prompts and reference outputs (AKA canonical / golden solutions) have **no requirements** in Bench. These components are only for your own analysis, and are not used by the scoring methods under the hood in code evaluation.

#### Unit tests

Unit tests must be compatible with the `code_eval` evaluator metric from [HuggingFace](https://huggingface.co/spaces/evaluate-metric/code_eval), which is what the `PythonUnitTesting` scoring method uses under the hood.

Here is the unit test for the `greatest_common_divisor` task from `HumanEval`:

```python
"\n\n\nMETADATA = {\n    'author': 'jt',\n    'dataset': 'test'\n}\n\n\ndef check(candidate):\n    assert candidate(3, 7) == 1\n    assert candidate(10, 15) == 5\n    assert candidate(49, 14) == 7\n    assert candidate(144, 60) == 12\n\ncheck(greatest_common_divisor)"
```

Here is what the unit test looks like if we remove the unnecessary metadata dict and print it out:

```python
def check(candidate):
    assert candidate(3, 7) == 1
    assert candidate(10, 15) == 5
    assert candidate(49, 14) == 7
    assert candidate(144, 60) == 12

check(greatest_common_divisor)
```

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

Unit tests can be passed to the `PythonUnitTesting` scorer as a list of strings as we did above, which is likely the simpler option if you are loading tests from a benchmark dataset (e.g. `HumanEval`):

```python
# create scorer from unit_test: List[str]
python_scorer = PythonUnitTesting(unit_tests=unit_tests)
```

Alternatively you can load unit tests from a directory to evaluate your candidate solutions.

Given a directory of unit test scripts:

```
unit_test_dir_name:
- unit_test_0.py
- unit_test_1.py
...
```

The `PythonUnitTesting` scorer can be created just from that directory name:

```python
# create scorer from unit_test_dir: str
python_scorer = PythonUnitTesting(unit_test_dir=unit_test_dir_name)

# create Test Suite same as before
python_suite = TestSuite(
    "humaneval_testsuite", # test suite name
    python_scorer, # scorer
    input_text_list=list(humaneval_df.prompt.values), # input prompts
    reference_output_list=list(humaneval_df.canonical_solution.values), # golden solutions
)
```

#### Solutions

Candidate solutions will only be evaluated to be correct if they contain:

- a function to call (in the HumanEval dataset, this is called the `entry_point`)
- any necessary imports

Here is an example ChatGPT-written solution for the greatest_common_divisor task:

```python
import math

def greatest_common_divisor(a: int, b: int) -> int:
    return math.gcd(a, b)
```

**Note:** this solution has a function `greatest_common_divisor` that the unit test above can invoke

**Note:** this solution has the `import math` statement at the top, which ChatGPT itself included as part of its solution. Without that `import math` statement, if we had ran the unit test on the solution code we would have gotten an error. Solutions are only evaluated to be correct if they include all their own imports!

### Best practices

#### Prompt Templating

Evaluation becomes more straightforward if you can easily extract the part of an LLM response which is its actual code solution. The simplest way to do that seems to be including an instruction in your prompt or system message that specifies to place code in between python markers in markdown, like this:

```python
<your code here>
```

We demonstrate an example of using this marker in the prompt template in the example below

#### Task description

Performance tends to improve on coding when your task description contains an explicit function signature that you want the solution to adhere to, as well as including example input/output behavior in its docstring

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

### Example

#### Load HumanEval dataset

Here we show how to download the HumanEval dataset from HuggingFace and load it as a pandas DataFrame

We will be using the `datasets` package. Make sure it is pip-installed before proceeding

```python
from datasets import load_dataset
import pandas as pd

humaneval_code_dataset = load_dataset("openai_humaneval")
humaneval_df = pd.DataFrame(humaneval_code_dataset["test"])
```

#### Generate solutions

Here is some example code that you can use to generate and compare coding solutions using OpenAI's GPT-3.5 and Anthropic's Claude-2

We will be using the OpenAI & Anthropic APIs. Make sure your environment variables for `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are configured before proceeding

```python
import openai
def chatgpt(input_text):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role" : "system", "content" : "You are a helpful assistant."},
            {"role" : "user", "content" : input_text}
        ],
        max_tokens=300
    )['choices'][0]['message']['content']

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
anthropic = Anthropic()
def claude(input_text):
    return anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=300,
        prompt=f"{HUMAN_PROMPT} {input_text} {AI_PROMPT}",
    ).completion

# used to extract the portion of an LLM response which is python code
extract_python = lambda x : x.replace('python\n', '').replace('```', '').replace(' def', 'def')

def get_solutions(model):

    prompt_template = """
    You are a bot that gives answers to coding tasks only. If the task is a coding task, give an expert python solution.
    If the task is unrelated, give the response "I don't know."
    ALWAYS mark the beginning and end of your solution with 
    ``python 
    and 
    ```
    Without these markers, the code cannot be extracted. Therefore the markers are required.
    ===
    <text>
    ===
    Solution:
    """
    filled_prompt_templates = [
        prompt_template.replace("<text>", humaneval_df[i]['prompt'])
        for i in range(len(humaneval_df))
    ]
    return [extract_python(model(x)) for x in filled_prompt_templates]

chatgpt_solutions = get_solutions(chatgpt)
claude_solutions = get_solutions(claude)
```

#### Create and run test suite

Now that you have generated solutions for each model, we can create a test suite and a run for each LLM

```python
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import PythonUnitTesting

# create scorer from unit_tests: List[str]
python_scorer = PythonUnitTesting(unit_tests=unit_tests)

# create test suite
python_suite = TestSuite(
    "humaneval_testsuite", 
    python_scorer,
    input_text_list=list(humaneval.prompt.values),
    reference_output_list=list(humaneval_df.canonical_solution.values),
)

# run test suite on GPT candidate solutions
python_suite.run(
    "chatgpt", # test run name
    candidate_output_list=chatgpt_solutions, # candidate solutions
)

# run test suite on Claude candidate solutions
python_suite.run(
    "claude", # test run name
    candidate_output_list=claude_solutions, # candidate solutions
)
```
