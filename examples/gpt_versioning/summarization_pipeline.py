import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from langchain.chains import LLMChain

from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import ScoringEnum

MODEL_VERSION = 'gpt-3.5-turbo-0301'
# MODEL_VERSION_TO_PROMOTE = 'gpt-3.5-turbo-0613'
MODEL_VERSION_TO_PROMOTE = 'gpt-3.5-turbo-16k'


def get_model(model_version):
    summary_llm = ChatOpenAI(temperature=0, model_name=model_version)
    system_message_prompt = SystemMessagePromptTemplate.from_template(
	"""You are an expert summarizer of text. A good summary 
	captures the most important information in the text and doesnt focus too much on small details."""
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        template="""Text: {text}
	                Summary:"""
    )

    summary_chain = LLMChain(llm=summary_llm, prompt=ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt]))

    return summary_chain


# load suite
news_suite = TestSuite("news_summary", ScoringEnum.SummaryQuality)
climate_suite = TestSuite("climate_summary", ScoringEnum.SummaryQuality)

# run inference
summary_chain = get_model(MODEL_VERSION_TO_PROMOTE)
news = []
climate = []
for input_ in news_suite.suite.test_cases:
    news.append(summary_chain({"text": input_.input})["text"])


for input_ in climate_suite.suite.test_cases:
    climate.append(summary_chain({"text": input_.input})["text"])

# score run
news_suite.run('gpt_35_16k', candidate_output_list=news, model_name=MODEL_VERSION_TO_PROMOTE)
climate_suite.run('gpt_35_16k', candidate_output_list=climate, model_name=MODEL_VERSION_TO_PROMOTE)

# save run