from collections import defaultdict
import pandas as pd

MOCK_DATAFRAME = pd.DataFrame(
    {   
        "input": [
            "this is test input to a language model",
            "this is another test prompt"
        ],
        "reference_output": [
            "this is test output from a language model",
            "this is a test response"
        ]
    }
)

MOCK_CUSTOM_DATAFRAME = MOCK_DATAFRAME.rename(columns={"input": "custom_prompt", "reference_output": "custom_reference"})

MOCK_INPUTS = [
    "this is test input to a language model",
    "this is another test prompt"
]

MOCK_REFERENCE_OUTPUTS = [
    "this is test output from a language model",
    "this is a test response"
]

MOCK_OUTPUTS = [
    'this is a test run output',
    'this is a good test run output',
]

MOCK_CODE_PASS = 'def add_1(x):\n    return x + 1'
MOCK_CODE_FAIL = 'def add_3(x):\n    return x + 2'

MOCK_UNIT_TEST_PASS = "def check(candidate):\n    assert(candidate(1) == 2)\ncheck(add_1)"
MOCK_UNIT_TEST_FAIL = "def check(candidate):\n    assert(candidate(1) == 4)\ncheck(add_3)"

MOCK_CODE_EVAL_RESULT_PASS = ({'pass@1': 1.0}, defaultdict(list, {0: [(0, {'task_id': 0, 'passed': True, 'result': 'passed', 'completion_id': 0})]}))
MOCK_CODE_EVAL_RESULT_FAIL = ({'pass@1': 0.0}, defaultdict(list, {0: [(0, {'task_id': 0, 'passed': False, 'result': 'failed: ', 'completion_id': 0})]}))