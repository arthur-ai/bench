## Using a custom scoring method 

In this guide, we will walk through the process of evaluating LLM performance using a custom scoring method. We will

1) Define a custom scorer
2) Create a test suite with that scorer
3) Run the test suite and view scores

### Define a custom scorer

All scorers in bench implement the {class}`Scorer <arthur_bench.scoring.scoring_method.ScoringMethod>` interface. Let's take a look at that interface:
```
class ScoringMethod(ABC):
    """
    Base class for all scorers. 
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
        :param context_batch: optional corresponding contexts, if needed by scorer
        """
        raise NotImplementedError
```
To create a custom scorer, we will implement the `name` and `run_batch` methods, and optionally override the `requires_reference` method if our scorer doesn't require reference or target data.

In the below example we create a custom scorer to check for repetition in a model generation. The scorer will accept an argument threshold, that specifies the maximum number of acceptable repetitions.
```
from nltk import trigrams

from arthur_bench.scoring import ScoringMethod

class TrigramRepetition(ScoringMethod):

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

### Using a custom scoring method in a test suite

In this section, we use our custom scorer to create a test suite. Our test suite is named `news_summary` and we pass the `TrigramRepetition` class that we defined above as the `scoring_method`.
Additionally, we provide a path to a csv file containing news articles to be used as model inputs during evaluation. Please see our {class}`documentation <arthur_bench.run.testsuite.TestSuite>` for all available data formats. 
```
from arthur_bench.run.testsuite import TestSuite

repetition_test = TestSuite('news_summary', scoring_method=TrigramRepetition(), reference_data_path='./example_summaries.csv')
```

### Run the test suite

Now that we've loaded in our custom scoring method, our test suite can be run as usual on any candidate generations.

```
run = repetition_test.run('test_run', candidate_output_list=['a great summary with no repetition!', 'a bad summary that repeats summary that repeats summary that repeats summary that repeats'])
print(run.test_cases)
```

```
>>> [TestCaseOutput(output='a great summary with no repetition!', score=1.0), TestCaseOutput(output='a bad summary that repeats summary that repeats summary that repeats summary that repeats summary that repeats', score=0.0)]
```

### Scoring Method Validation

Test suites expect scoring method configurations to remain consistent from run to run, so that each runs scores can be compared and reliably tracked throughout time. Let's see what happens if we attempt to use this suite at a later time, but edit the underlying parameters.

```
scorer = TrigramRepetition(threshold=7)
repetition_test = TestSuite('news_summary', scoring_method=scorer)
```

We see the following warning:

```
scoring method configuration has changed from test suite creation.
```

By default, bench will save the json serializable attributes of your scoring method as the configuration. If you need more advanced serialization for validation or re-initialization, implement the `to_dict()` and `from_dict()` methods on your custom class. You can find the full ScoringMethod spec {class}`here <arthur_bench.scoring.scoring_method.ScoringMethod>`.

If you think you've got a useful scoring method, please consider [contributing](contributing.md)!