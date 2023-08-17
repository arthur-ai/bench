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

```python
import pandas as pd
from datasets import load_dataset
billsum = load_dataset("billsum", split="ca_test")
billsum_df = pd.DataFrame(billsum).sample(10, random_state=278487)
```

## LLM response generation

We use different temperature settings to generate three different lists of responses:

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

gpt3 = OpenAI(temperature=0.0, max_tokens=500)

prompt_template_old = PromptTemplate(
	input_variables=["text"],
	template="""
	What are the basics of this text?
	Text: {text}
	Summary:
	"""
)

prompt_template_new = PromptTemplate(
	input_variables=["text"],
	template="""
	You are an expert summarizer of legal text. A good summary 
	captures the most important information in the text and doesnt focus too much on small details.
	Make sure to use your expert legal knowledge in summarizing.
	Text: {text}
	Summary:
	"""
)

gpt3_prompt_old_chain = LLMChain(llm=gpt3, prompt=prompt_template_old)
gpt3_prompt_new_chain = LLMChain(llm=gpt3, prompt=prompt_template_new)

# generate summaries with truncated text
prompt0_summaries = [gpt3_prompt_old_chain({"text": bill[:3000]})["text"] for bill in billsum_df.text]
prompt1_summaries = [gpt3_prompt_new_chain({"text": bill[:3000]})["text"] for bill in billsum_df.text]
```

## Create test suite

For this test suite, we want to compare `gpt-3` against `command`. We will use the BERTScore scoring metric to measure how much the candidate summaries approach the reference summaries as we increase the amount of use-case specific detail in the prompt.

```python
from arthur_bench.run import TestSuite
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
