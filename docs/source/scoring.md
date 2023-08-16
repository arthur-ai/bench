## Scoring

A **Scoring Method** is the criteria used to quantitatively evaluate LLM outputs. When you test LLMs with Arthur Bench, you attach a Scoring Method to each test suite you create - this defines how performance will be measured consistently across that test suite.

Here is a list of all the scoring methods available by default in Arthur Bench (listed alphabetically):

| Scoring Method                    | Tasks | Requirements |
|-----------------------------------|-----|-----|
| BERT Score (`bertscore`)          | any | Reference Output, Candidate Output|
| Exact Match (`exact_match`)       | any | Reference Output, Candidate Output|
| Hedging Language (`hedging_language`)   | any | Candidate Output |
| Python Unit Testing (`python_unit_testing`)   | Python Generation | Candidate Output, Unit Tests (see the [code eval guide](code_eval.md)) |
| QA Correctness (`qa_correctness`) | Question-Answering| Input, Candidate Output, Context|
| Readability (`readability`)       | any | Candidate Output |
| Specificity (`specificity`)       | any | Candidate Output |
| Summary Quality (`summary_quality`)  | Summarization | Input, Reference Output, Candidate Output|
| Word Count Match (`word_count_match`)   | any | Reference Output, Candidate Output |


For better understandability we have broken down the scorers by the type of procedure each scorer uses

### Scoring methods that use prompting

| Scoring Method                    | Tasks | Requirements |
|-----------------------------------|-----|-----|
| QA Correctness (`qa_correctness`) | Question-Answering| Input, Candidate Output, Context|
| Summary Quality (`summary_quality`)  | Summarization | Input, Reference Output, Candidate Output|

### Scoring methods that use embedding-similarity

| Scoring Method                    | Tasks | Requirements |
|-----------------------------------|-----|-----|
| BERT Score (`bertscore`)          | any | Reference Output, Candidate Output|
| Hedging Language (`hedging_language`)   | any | Candidate Output |

### Scoring methods that use word presence, frequency, & complexity

| Scoring Method                    | Tasks | Requirements |
|-----------------------------------|-----|-----|
| Exact Match (`exact_match`)       | any | Reference Output, Candidate Output|
| Readability (`readability`)       | any | Candidate Output |
| Specificity (`specificity`)       | any | Candidate Output |
| Word Count Match (`word_count_match`)   | any | Reference Output, Candidate Output |

### Scoring methods that evaluate code

| Scoring Method                    | Tasks | Requirements |
|-----------------------------------|-----|-----|
| Python Unit Testing (`python_unit_testing`)   | Python Generation | Candidate Output, Unit Tests (see the [code eval guide](code_eval.md)) |


For a walkthrough on how to extend the ScoringMethod class to create your own scorer specialized to your data and/or use-case to use with Arthur Bench, check out the [custom scoring guide](custom_scoring.md)

If you would like to contribute scoring methods to the open source Arthur Bench repo, check out our [contributing guide](contributing.md)

### Scoring methods that use prompting

#### `qa_correctness`

The QA correctness scorer evaluates the correctness of an answer, given a question and context. This scoring method does not require a reference output, but does require context. Each row of the Test Run will receive a binary 0, indicating an incorrect output, or 1, indicating a correct output.

#### `summary_quality`

The Summary Quality scorer evaluates a summary against its source text and a reference summary for comparison. It evaluates summaries on dimensions including relevance and syntax. Each row of the test run will receive a binary 0, indicating that the reference output was scored higher than the candidate output, or 1, indicating that the candidate output was scored higher than the reference output.

### Scoring methods that use embedding-similarity

#### `bertscore`

[BERTScore](https://arxiv.org/abs/1904.09675) is a quantitative metric to compare the similarity of two pieces of text. Using the `bertscore` scoring method will score each row of the test run as the bert score between the reference output and the candidate output.

#### `hedging_language`

The Hedging Language scoring method evaluates whether a candidate response is similar to generic hedging language used by an LLM ("As an AI language model, I don't have personal opinions, emotions, or beliefs"). Each row of the Test Run will receive a binary 0, indicating hedging language *not* used, or 1, indicating hedging language used. These binary values are determined based on the BERTScore between the candidate response and the hedging language - if the similarity is below a threshold, the score is 0, and otherwise if the similarity is above the threshold, the score is 1. The threshold we use by default with this scorer is calibrated to the empirical distribution of BERTScore on hedging language overall.

### Scoring methods that use word presence, frequency, & complexity

#### `exact_match`

The Exact Match scorer evaluates whether the candidate output exactly matches the reference output. This is case sensitive. Each row of the Test Run will receive a binary 0, indicating a non-match, or 1, indicating an exact match.

#### `readability`

The Readability scorer evaluates the reading ease of the candidate output according to the [Flesch Reading Ease Score](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests). The higher the score, the easier the candidate output is to read: scores of 90-100 correlate to a 5th grade reading level, while scores less than 10 are classified as being "extremely difficult to read, and best understood by university graduates."

#### `specificity`

The Specificity scorer outputs a score of 0 to 1, where smaller values correspond to candidate outputs with more vague language while higher values correspond to candidate outputs with more precise language. Specificity is calculated through 3 heuristic approaches: identifying the presence of predefined words that indicate vagueness, determing how rare the words used are according to word frequencies calculated by popular NLP corpora, and detecting the use of proper nouns and numbers.

#### `word_count_match`

For scenarios where there is a preferred output length, `word_count_match` calculates a corresponding score on the scale of 0 to 1. Specifically, this scoring method calculates how similar the number of words in the candidate output is to the number of words in the reference output, where a score of 1.0 indicates that there are the same number of words in the candidate output as in the reference output. Scores less than 1.0 are calculated as ((len_reference-delta)/len_reference) where delta is the absolute difference in word lengths between the candidate and reference outputs. All negative computed values are truncated to 0. 

### Scoring methods that evaluate code

#### `python_unit_testing`

The Python Unit Testing scorer evaluates candidate solutions to coding tasks against unit tests. This scoring method wraps the [`code_eval`](https://huggingface.co/spaces/evaluate-metric/code_eval) evaluator interface from HuggingFace. It is important to note that this function requires that solution code uses standard python libraries only.