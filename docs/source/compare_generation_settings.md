# Compare Generation Settings

In this guide we compare LLM-generated answers to questions using different temperature settings. Higher temperature improves creativity and diversity of answers, but increases the likelihood that responses veer into nonsense.

We use a custom scorer that compares each LLM temperature setting based on how many typos each response contains

## Environment setup

In this guide, we use the OpenAI API and use the `pyspellchecker` package for a custom scoring method
```
export OPENAI_API_KEY="sk-..."
pip install pyspellchecker
```

## Data preparation

We write out some basic questions which we will use to test how much temperature impacts the responses

```python
inputs = ["What planet are we on?", "What time is it?", "What day is it?", "What is love?"]
```

## LLM response generation

We use different temperature settings to generate three different lists of responses:

```python
from langchain.chat_models import ChatOpenAI
chatgpt_zero_temp = ChatOpenAI(temperature=0.0, max_tokens=100)
chatgpt_low_temp = ChatOpenAI(temperature=0.5, max_tokens=100)
chatgpt_med_temp = ChatOpenAI(temperature=1.2, max_tokens=100)
chatgpt_high_temp = ChatOpenAI(temperature=1.9, max_tokens=100)

baseline_responses = [chatgpt_zero_temp.predict(x) for x in inputs]
low_temp_responses = [chatgpt_low_temp.predict(x) for x in inputs]
med_temp_responses = [chatgpt_med_temp.predict(x) for x in inputs]
high_temp_responses = [chatgpt_high_temp.predict(x) for x in inputs]
```

## Create test suite

For this test suite, we want to measure how corrupted the responses get as we increase the generation temperature.

Let's define a quick custom scoring method that uses the `pyspellchecker` package to scan for typos in the response, and we will then see how much the typo score changes between the low, medium, and high temperature model generations.

```python
from arthur_bench.scoring import ScoringMethod
from spellchecker import SpellChecker
import string
from typing import List, Optional

class CustomSpellingScore(ScoringMethod):
    """
    Custom scoring which scores each LLM response with the formula 1 / (2 ^ number of typos)
    This gives a typo-free response a score of 1, and each additional typo further decreases the score
    """

	def __init__(self):
		self.spell_checker = SpellChecker()

	@staticmethod
	def name() -> str:
		return "spell_checker"

	@staticmethod
	def requires_reference() -> bool:
		return False
	
	def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None,
				  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
		res = []
		for s in candidate_batch:

			# remove punctuation
			s = ''.join(ch for ch in s if ch not in string.punctuation)

			# get number of typos in s
			num_typos = len(self.spell_checker.unknown(s.split()))

			# custom score is 1/(2^num_typos)
			res.append(1.0 / (2**num_typos))
		return res

my_suite = TestSuite(
	"test-spelling", 
	CustomSpellingScore(), 
    input_text_list=inputs,
	reference_output_list=baseline_responses
)
```

## Run test suite

```python
my_suite.run("low_temp_responses", candidate_output_list=low_temp_responses)
my_suite.run("med_temp_responses", candidate_output_list=med_temp_responses)
my_suite.run("high_temp_responses", candidate_output_list=high_temp_responses)
```

## View results

Run `bench` from your command line to visualize the run results comparing the different temperature settings.
