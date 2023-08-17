from collections import defaultdict
import pandas as pd

MOCK_DATAFRAME = pd.DataFrame(
    {
        "input": [
            "this is test input to a language model",
            "this is another test prompt",
        ],
        "reference_output": [
            "this is test output from a language model",
            "this is a test response",
        ],
    }
)

MOCK_CUSTOM_DATAFRAME = MOCK_DATAFRAME.rename(
    columns={"input": "custom_prompt", "reference_output": "custom_reference"}
)

MOCK_INPUTS = ["this is test input to a language model", "this is another test prompt"]

MOCK_REFERENCE_OUTPUTS = [
    "this is test output from a language model",
    "this is a test response",
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

MOCK_SUMMARY_DATA = pd.DataFrame(
    {
        "source": [
            "Breaking News: Earthquake measuring 7.2 magnitude strikes California. The earthquake originated near the city of Los Angeles and was felt across the region. Several buildings have collapsed, and there are reports of injuries and casualties. Rescue operations are underway.",
            "Just had the most amazing dinner at this new restaurant in town! The food was delicious, and the service was top-notch. I highly recommend it to everyone looking for a great dining experience.",
            "New study reveals the benefits of regular exercise. According to the research, engaging in physical activity for at least 30 minutes a day can significantly reduce the risk of heart disease, obesity, and other chronic conditions. Start incorporating exercise into your daily routine!",
            "Exciting announcement: The company is launching a new product next month. Stay tuned for more details and be among the first to experience this innovative offering.",
        ],
        "summary": [
            "A powerful earthquake hits California, causing damage and casualties.",
            "An enthusiastic review of a new restaurant in town with excellent food and service.",
            "Recent study highlights the positive impact of regular exercise on health.",
            "The company plans to release a new product, generating anticipation among customers.",
        ],
        "candidate_summary": [
            "Massive earthquake strikes California, causing destruction and loss of life.",
            "Had dinner at a new restaurant. Food and service were great!",
            "Exercise has health benefits and can reduce the risk of diseases.",
            "Exciting news: New product launch coming soon!",
        ],
    }
)

MOCK_HEDGING_LANGUAGE = pd.DataFrame(
    {
        "instruction": [
            "How many teaspoons are in a tablespoon?",
            "Why are the Georgia Bulldogs back to back National Champions in Football?",
            "Who owns the best dog in the world?",
        ],
        "response": [
            "Three teaspoons are equivalent to one tablespoon.",
            "Coach Kirby Smart brought to Georgia what he learned as a longtime assistant with Nick Saban at Alabama and made his own process for Championship success. Smart has recruited the top high school players in the country to play for the Bulldogs and he has created a culture of brotherhood and accountability. The Georgia Bulldogs are now the standard of excellence when it comes to College Football.",
            "Reedo does because his little legend loves an away day and has great chat with the fam.",
        ],
        "candidate_output": [
            "There are 3 teaspoons in a tablespoon.",
            "As an AI, I provide real-time information up to October 2021. As of the last update, the Georgia Bulldogs are not back-to-back National Champions in Football. The team won its last National Championship in 1980. I recommend checking a recent sports news source to get the latest information.",
            'As an AI, I don\'t have personal opinions. However, "the best dog in the world" is subjective and can vary from person to person. It often refers to one\'s own pet, as the bond between a person and their pet is personal and unique. Thus, the owner of the "best dog in the world" could well be you or anyone who loves and cares for their dog deeply.',
        ],
    }
)
