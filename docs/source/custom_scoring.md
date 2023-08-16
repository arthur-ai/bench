# Custom Scoring

In this guide, we will walk through the process of evaluating LLM performance using a custom scoring method. We will

1) Define a custom scoring method
2) Create a test suite with that scoring method
3) Run the test suite and view scores

## Define a custom scoring method

All scoring methods in bench implement the {class}`scoring method <arthur_bench.scoring.scoring_method.ScoringMethod>` interface. Let's take a look at that interface:
```python
class ScoringMethod(ABC):
    """
    Base class for all scoring methods.     
    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        Get the name of this ScoringMethod
        :return: the ScoringMethod name
        """
        raise NotImplementedError
    
    @staticmethod
    def requires_reference() -> bool:
        return True

    @abstractmethod
    def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None,
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        """
        Score a batch of candidate generations.

        :param candidate_batch: candidate generations to score
        :param reference_batch: reference strings representing target outputs
        :param input_text_batch: optional corresponding inputs
        :param context_batch: optional corresponding contexts, if needed by scoring method 
        """
        raise NotImplementedError
```
To create a custom scorer, we will implement the `name` and `run_batch` methods, and optionally override the `requires_reference` method if our scoring method doesn't require reference or target data.

In the below example we create a custom scorer to check for repetition in a model generation.
```python
from arthur_bench.scoring import ScoringMethod
from nltk import trigrams
from typing import List, Optional

class TrigramRepetition(ScoringMethod):
    @staticmethod
    def name() -> str:
        return "trigram_repetition"

    @staticmethod
    def requires_reference() -> bool:
        return False
    
    def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None,
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        repeat_scores = []
        for text in candidate_batch:
            tokens = [t.lower() for t in nltk.word_tokenize(text)]
            all_trigrams = trigrams(tokens)
            counts = {}
            for tri in all_trigrams:
                if tri in counts:
                    counts[tri] += 1
                else:
                    counts[tri] = 1
            max_repeat = max(counts.values())
            repeat_scores.append(float(max_repeat < 5))
        return repeat_scores
```

## Using a custom scoring method in a test suite

In this section, we use our custom scoring method to create a test suite. Our test suite is named `news_summary` and we pass the `TrigramRepetition` class that we defined above as the `scoring_method`.
Additionally, we provide a path to a csv file containing news articles to be used as model inputs during evaluation. Please see our {class}`documentation <arthur_bench.run.testsuite.TestSuite>` for all available data formats. 
```python
from arthur_bench.run.testsuite import TestSuite

repetition_test = TestSuite('news_summary', scoring_method=TrigramRepetition, reference_data_path='./examples/data/news_summary/example_summaries.csv')
```

## Run the test suite

Now that we've loaded in our custom scoring method, our test suite can be run as usual on any candidate generations.

```python
run = repetition_test.run('test_run', candidate_output_list=['a great summary with no repetition!', 'a bad summary that repeats summary that repeats summary that repeats summary that repeats'])
print(run.test_case_outputs)
```

```python
>>> [TestCaseOutput(output='a great summary with no repetition!', score=1.0), TestCaseOutput(output='a bad summary that repeats summary that repeats summary that repeats summary that repeats summary that repeats', score=0.0)]
```

If you think you've got a useful scoring method, please consider [contributing](contributing.md)!
