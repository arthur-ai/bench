# Compare LLM Providers

In this guide we compare LLMs answers at summarizing text.

## Environment setup

In this guide, we use the OpenAI API and the Cohere API
```
pip install openai cohere
export OPENAI_API_KEY="sk-..."
export COHERE_API_KEY="..."
```

## Data preparation

We load a publically available [congressional bill summarization dataset](https://huggingface.co/datasets/billsum) from HuggingFace.

```python
import pandas as pd
from datasets import load_dataset
billsum = load_dataset("billsum", split="ca_test")
billsum_df = pd.DataFrame(billsum).sample(10, random_state=278487)
```

## LLM response generation

We use different temperature settings to generate three different lists of responses:

```python
from langchain.llms import OpenAI, Cohere
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

gpt3 = OpenAI(temperature=0.0, max_tokens=100)
command = Cohere(temperature=0.5, max_tokens=100)

prompt_template = PromptTemplate(
	input_variables=["text"],
	template="""
	You are an expert summarizer of text. A good summary 
	captures the most important information in the text and doesnt focus too much on small details.
	Text: {text}
	Summary:
	"""
)

gpt3_chain = LLMChain(llm=gpt3, prompt=prompt_template)
command_chain = LLMChain(llm=command, prompt=prompt_template)

# generate summaries with truncated text
gpt3_summaries = [gpt3_chain({"text": bill[:3000]})["text"] for bill in billsum_df.text]
command_summaries = [command_chain({"text": bill[:3000]})["text"] for bill in billsum_df.text]
```

## Create test suite

For this test suite, we want to compare `gpt-3` against `command`. We will use the SummaryQuality scoring metric to A/B test each set of candidate responses against the reference summaries from the dataset

```python
from arthur_bench.run.testsuite import TestSuite
my_suite = TestSuite(
	"congressional_bills", 
	"summary_quality", 
	input_text_list=list(billsum_df.text),
	reference_output_list=list(billsum_df.summary)
)
```

## Run test suite

```python
my_suite.run("gpt3_summaries", candidate_output_list=gpt3_summaries)
my_suite.run("command_summaries", candidate_output_list=command_summaries)
```

## View results

Run `bench` from your command line to visualize the run results comparing the different temperature settings.
