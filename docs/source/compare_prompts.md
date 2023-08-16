## Compare Prompts

Outline

- env
- test suite data
- get LLM responses
- make test suite
- run tests on each set of responses
- view results

This guide provides a step by step tutorial on LLM evaluation with the Bench SaaS platform. It can be run in local mode by skipping step 1, and use the cli to view results. To get started with key bench concepts like test suites, test runs, and scoring methods, check out [this page](concepts.md) first. 

In this example, we will use the bench library to get started evaluating different LLMs for news article summarization and log the results to the Arthur Bench platform. We will walk through the following steps:

1) Configuring your python environment for logging results.

2) Creating an initial test suite of reference examples for evaluation.

3) Running the test suite on a set of candidate model generations. In this example, we will compare the performance of an open source summarization model.

4) Viewing and analyzing the results

### Configuring your python environment

Set the following environment variables to enable logging results:
```
import os
os.environ['ARTHUR_API_URL'] = 'https://app.arthur.ai'
os.environ['ARTHUR_API_KEY'] = 'YOUR API KEY'
```

### Creating an initial test suite
We recommend creating a test suite with target  examples as close to production performance as possible. For the news summarization case, we will assume we have sampled news articles from the past week as inputs. Reference outputs can be hard to find, so will initialize a baseline using gpt3.5. You can download the summaries file from our Github.

To generate the reference outputs
	1) Load the input articles from csv to Pandas DataFrame
	2) Use LangChain to define a prompt template and manage requests to OpenAI
	3) Generate and save summaries for each article

```
import pandas as pd
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


articles = pd.read_csv('example_summaries.csv')['input_text']
reference_summaries = []
summary_llm = OpenAI(temperature=0)
model = LLMChain(llm=summary_llm, prompt=PromptTemplate(
	input_variables=["text"],
	template="""
	You are an expert summarizer of text. A good summary 
	captures the most important information in the text and doesnt focus too much on small details.
	Text: {text}
	Summary:
	"""
))

for article in articles:
    reference_summaries.append(model({"text": article[:3000]})["text"])
```

Now that we have a set of input articles and reference summaries we can create a test suite for benchmarking.

```
from arthur_bench.run.testsuite import TestSuite

news_summary_test = TestSuite(name='news_summary', scoring_method='summary_quality', input_text_list=articles, reference_output_list=reference_summaries)
```

If you have previous generations you'd like to use for creating a test suite, please see our {class}`documentation <arthur_bench.run.testsuite.TestSuite>` for all compatible data formats.

### Running the test suite
For the first run, we will evaluate the performance of an open source model relative to the generations of gpt3. In this example we will use a t5 model trained on book summarization available on the huggingface hub:

```
from transformers import pipeline

pipe = pipeline("summarization", model="pszemraj/long-t5-tglobal-base-16384-book-summary")

def model(text):
    prompt = f"You are an expert summarizer of text. A good summary captures the most important information in the text and doesnt focus too much on small details. Summarize this text: {text}"
    return pipe(prompt)
```

Next, generate a response for each input in the test suite. Run the suite to score each generation.
```
candidate_generations = []
for test_case in news_summary_test.suite.test_cases:
    candidate_generations.append(model(test_case.input)[0]["summary_text"])

suite.run(run_name='t5_books', candidate_output_list=candidate_generations, model_name='long-t5-tglobal-base-16384-book-summary')
```

### Viewing and analyzing the results

Log in to your Arthur account to view in depth run result tables, test run distributions, and averages.
TODO: screenshots with exampels of high scores and low scores

To get test suite statistics locally run:
```
statistics = suite.client.get_summary_statistics(suite.id)
```