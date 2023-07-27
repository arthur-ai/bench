## Evaluating LLM generated summaries with Bench

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
We recommend creating a test suite with target  examples as close to production performance as possible. For the news summarization case, we will assume we have sampled news articles from the past week as inputs. Reference outputs can be hard to find, so will initialize a baseline using gpt3.5.

```
import pandas as pd
from langchain.llms import Cohere, HuggingFacePipeline, OpenAI
from langchain.chains import LLMChain


articles = pd.read_csv('example_summaries.csv)['input_text']
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
    reference_summaries.append(model({"text": artcile})["text"])

```



```
from arthur_bench.run.testsuite import TestSuite

suite = TestSuite(name='news_summary', scoring_method='summary_quality')
```

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
for test_case in suite.test_cases:
    candidate_generations.append(model(test_case.input)[0]["summary_text"])

suite.run(candidate_output_list=candidate_generations)
```

### Viewing and analyzing the results