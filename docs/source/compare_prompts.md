# Compare Prompts

In this guide we compare prompts 

## Environment setup

In this guide, we use the OpenAI API
```
pip install openai
export OPENAI_API_KEY="sk-..."
```

## Data preparation

We load a publically available [congressional bill summarization dataset](https://huggingface.co/datasets/billsum) from HuggingFace.

We also prepare an example bill with its summary to include in a prompt as an example response.

```python
import pandas as pd
from datasets import load_dataset
billsum = load_dataset("billsum")
billsum_df = pd.DataFrame(billsum["ca_test"]).sample(10, random_state=278487)
example_bill = billsum["test"][6]["text"]
example_bill_summary = billsum["test"][6]["summary"]
```

## LLM response generation

We use different temperature settings to generate three different lists of responses:

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

gpt35 = ChatOpenAI(temperature=0.0, max_tokens=100)

prompt0_template= PromptTemplate(
	input_variables=["text"],
	template="""
	Text: {text}
	Summary:
	"""
)

prompt1_template = PromptTemplate(
	input_variables=["text", "example_bill", "example_bill_summary"],
	template="""
	You are an expert summarizer of legal text. A good summary 
	captures the most important information in the text and doesnt focus too much on small details.
	Make sure to use your expert legal knowledge in summarizing.
	===
	Text: {example_bill}
	Summary: {example_bill_summary}
	===
	Text: {text}
	Summary:
	"""
)

prompt0_chain = LLMChain(llm=gpt35, prompt=prompt0_template)
prompt1_chain = LLMChain(llm=gpt35, prompt=prompt1_template)


# generate summaries with truncated text
prompt0_summaries = [prompt0_chain.run(bill[:3000]) for bill in billsum_df.text]
prompt1_summaries = [
	prompt1_chain({"text" : bill[:3000], "example_bill" : example_bill, "example_bill_summary" : example_bill_summary})["text"]
	for bill in billsum_df.text
]
```

## Create test suite

For this test suite, we will use the BERTScore scoring metric to measure how much the candidate summaries approach the reference summaries by upgrading our prompt with task-specific detail and an example.

```python
from arthur_bench.run.testsuite import TestSuite
my_suite = TestSuite(
	"congressional_bills_to_reference", 
	"bertscore", 
	input_text_list=list(billsum_df.text),
	reference_output_list=list(billsum_df.summary)
)
```

## Run test suite

```python
my_suite.run("prompt0_summaries", candidate_output_list=prompt0_summaries)
my_suite.run("prompt1_summaries", candidate_output_list=prompt1_summaries)
```

## View results

Run `bench` from your command line to visualize the run results comparing the different temperature settings.
