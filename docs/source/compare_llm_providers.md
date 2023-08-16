## Compare LLM providers

Outline

In this guide we compare LLM-generated summaries using three different LLM providers, using `gpt-3.5-turbo` as a baseline and then evaluating `claude-2` and a free HuggingFace model as candidates.

We use the SummaryQuality scoring method to measure how often the SummaryQuality scorer (which uses `gpt-3.5-turbo` as an evaluator) prefers the candidates over the baseline in an A/B test.

- env
- test suite data
- get LLM responses
- make test suite
- run tests on each set of responses
- view results


env
```
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-..."
```

test suite data

```python

```


LLM responses

```python

```

make test suite

```python

```

run tests on each set of responses

```python

```

view results

```python

```
