# Custom Scoring

In this guide, we will walk through the process of evaluating LLM performance using a custom scorer. We will

1) Define a custom scorer
2) Create a test suite with that scorer
3) Run the test suite and view scores


## Define a custom scorer

To create a custom scorer, we will implement the `name` and `run_batch` methods, and optionally override the `requires_reference` method if our scorer doesn't require reference or target data.

This example custom scorer is called `TrigramRepitition`, which scores responses with a 0.0 if they contain repeated trigrams above a thresholded number of times.

```python
from arthur_bench.scoring import Scorer
from nltk import trigrams
from typing import List, Optional

class TrigramRepetition(Scorer):

    def __init__(self, threshold: int = 5):
        self.threshold = threshold
    
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
            repeat_scores.append(float(max_repeat < self.threshold))
        return repeat_scores
```

## Using a custom scorer in a test suite


We pass in our custom scorer as the `scoring_method` parameter to the test suite:

```python
from arthur_bench.run.testsuite import TestSuite

repetition_test = TestSuite(
    'custom_trigram_suite', 
    scoring_method=TrigramRepetition(), 
    input_text_list=[
        "Talk to me but don't repeat yourself too much", 
        "Talk to me but don't repeat yourself too much"
    ]
)   
```

## Run the test suite

Now that we've loaded in our custom scorer, our test suite can be run as usual on any candidate generations.

```python
run = repetition_test.run(
    'test_run', 
    candidate_output_list=[
        'a great response with no repetition!', 
        'a bad response that repeats response that repeats response that repeats response that repeats'
    ]
)
print(run.scores)
```

```python
>>> [1.0, 0.0]
```

## Scorer Validation

Test suites expect scorer configurations to remain consistent from run to run, so that each runs scores can be compared and reliably tracked throughout time. Let's see what happens if we attempt to use this suite at a later time, but edit the underlying parameters.

```python
scorer = TrigramRepetition(threshold=7)
repetition_test = TestSuite('custom_trigram_suite', scoring_method=scorer)
```

We see the following warning:

```
scoring method configuration has changed from test suite creation.
```

By default, bench will save the json serializable attributes of your scorer as the configuration. If you need more advanced serialization for validation or re-initialization, implement the `to_dict()` and `from_dict()` methods on your custom class. You can find the full scorer spec {class}`here <arthur_bench.scoring.scorer.Scorer>`.

## `Scorer` interface

All scorers in bench implement the {class}`scorer <arthur_bench.scoring.scorer.scorer>` interface. Let's take a look at that interface:
```python
class Scorer(ABC):
    """
    Base class for all scorers.     
    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        Get the name of this Scorer
        :return: the Scorer name
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
        :param context_batch: optional corresponding contexts, if needed by scorer 
        """
        raise NotImplementedError
```
To create a custom scorer, you need to implement the `name` and `run_batch` methods, and optionally override the `requires_reference` method if your scorer doesn't require reference or target data.

## Contributing

If you think you've got a useful scorer, please consider [contributing](contributing.md)!
