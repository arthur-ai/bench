# Scoring

A **Scorer** is the criteria used to quantitatively evaluate LLM outputs. When you test LLMs with Arthur Bench, you attach a Scorer to each test suite you create - this defines how performance will be measured consistently across that test suite.

For a walkthrough on how to extend the Scorer class to create your own scorer specialized to your data and/or use-case to use with Arthur Bench, check out the [custom scoring guide](custom_scoring.md)

If you would like to contribute scorers to the open source Arthur Bench repo, check out our [contributing guide](contributing.md)

Here is a list of all the scorers available by default in Arthur Bench (listed alphabetically):

| Scorer                    | Tasks | Type | Requirements | 
|-----------------------------------|-----|-----|-----|
| BERT Score (`bertscore`)          | any |  Embedding-Based | Reference Output, Candidate Output|
| Exact Match (`exact_match`)       | any | Lexicon-Based | Reference Output, Candidate Output|
| Hallucination (`hallucination`)       | any | Prompt-Based | Candidate Output, Context|
| Hedging Language (`hedging_language`)   | any | Embedding-Based | Candidate Output |
| Python Unit Testing (`python_unit_testing`)   | Python Generation | Code Evaluator| Candidate Output, Unit Tests (see the [code eval guide](code_evaluation.md)) |
| QA Correctness (`qa_correctness`) | Question-Answering| Prompt-Based | Input, Candidate Output, Context|
| Readability (`readability`)       | any | Lexicon-Based | Candidate Output |
| Specificity (`specificity`)       | any | Lexicon-Based | Candidate Output |
| Summary Quality (`summary_quality`)  | Summarization |Prompt-Based  | Input, Reference Output, Candidate Output|
| Word Count Match (`word_count_match`)   | any |Lexicon-Based | Reference Output, Candidate Output |


For better understandability we have broken down the Scorers based on the type of procedure each Scorer uses.

## Prompt-Based Scorers

### `qa_correctness`

The QA correctness scorer evaluates the correctness of an answer, given a question and context. This scorer does not require a reference output, but does require context. Each row of the Test Run will receive a binary 0, indicating an incorrect output, or 1, indicating a correct output.

### `summary_quality`

The Summary Quality scorer evaluates a summary against its source text and a reference summary for comparison. It evaluates summaries on dimensions including relevance and syntax. Each row of the test run will receive a binary 0, indicating that the reference output was scored higher than the candidate output, or 1, indicating that the candidate output was scored higher than the reference output.

### `hallucination`

The Hallucination scorer takes a response and a context (e.g. in a RAG setting where context is used to ground an LLM’s responses) and identifies when information in the response is not substantiated by the context . The scorer breaks down the response into a list of claims and checks the claims against the context for support. This binary score is 0 if all claims are supported, and 1 otherwise.

## Embedding-Based Scorers

### `bertscore`

[BERTScore](https://arxiv.org/abs/1904.09675) is a quantitative metric to compare the similarity of two pieces of text. Using `bertscore` will score each row of the test run as the bert score between the reference output and the candidate output.

### `hedging_language`

The Hedging Language scorer evaluates whether a candidate response is similar to generic hedging language used by an LLM ("As an AI language model, I don't have personal opinions, emotions, or beliefs"). Each row of the Test Run will receive a score between 0.0 and 1.0 indicating the extent to which hedging language is detected in the response (using BERTScore similarity to the target hedging phrase). A score above 0.5 typically suggests the model output contains hedging language.

## Lexicon-Based Scorers

### `exact_match`

The Exact Match scorer evaluates whether the candidate output exactly matches the reference output. This is case sensitive. Each row of the Test Run will receive a binary 0, indicating a non-match, or 1, indicating an exact match.

### `readability`

The Readability scorer evaluates the reading ease of the candidate output according to the [Flesch Reading Ease Score](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests). The higher the score, the easier the candidate output is to read: scores of 90-100 correlate to a 5th grade reading level, while scores less than 10 are classified as being "extremely difficult to read, and best understood by university graduates."

### `specificity`

The Specificity scorer outputs a score of 0 to 1, where smaller values correspond to candidate outputs with more vague language while higher values correspond to candidate outputs with more precise language. Specificity is calculated through 3 heuristic approaches: identifying the presence of predefined words that indicate vagueness, determing how rare the words used are according to word frequencies calculated by popular NLP corpora, and detecting the use of proper nouns and numbers.

### `word_count_match`

For scenarios where there is a preferred output length, `word_count_match` calculates a corresponding score on the scale of 0 to 1. Specifically, this scorers calculates how similar the number of words in the candidate output is to the number of words in the reference output, where a score of 1.0 indicates that there are the same number of words in the candidate output as in the reference output. Scores less than 1.0 are calculated as ((len_reference-delta)/len_reference) where delta is the absolute difference in word lengths between the candidate and reference outputs. All negative computed values are truncated to 0. 

## Code Evaluators

### `python_unit_testing`

The Python Unit Testing scorer evaluates candidate solutions to coding tasks against unit tests. This scorer wraps the [`code_eval`](https://huggingface.co/spaces/evaluate-metric/code_eval) evaluator interface from HuggingFace. It is important to note that this function requires that solution code uses standard python libraries only.
