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