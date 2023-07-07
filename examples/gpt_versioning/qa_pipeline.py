import pickle
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import ScoringEnum

MODEL_VERSION = 'gpt-3.5-turbo-0301'
MODEL_VERSION_TO_PROMOTE = 'gpt-3.5-turbo-0613'
# MODEL_VERSION_TO_PROMOTE = 'gpt-3.5-turbo-16k'

ml_suite = TestSuite('ml_paper_qa', scoring_method=ScoringEnum.QACorrectness)
climate_suite = TestSuite('climate_qa', scoring_method=ScoringEnum.QACorrectness)

def get_model(model_version, filestore):
    openai_llm = ChatOpenAI(model_name=model_version)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(filestore, embeddings)
    ml_qa = RetrievalQAWithSourcesChain.from_chain_type(
        llm=openai_llm, 
        chain_type="stuff", 
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
        )  
    return ml_qa 

ml_paper = get_model(MODEL_VERSION, 'ml_papers_index')
climate_qa = get_model(MODEL_VERSION, 'climate_index')

answers = []
context = []
for paper in ml_suite.suite.test_cases:
    res = ml_paper(paper.input)
    answers.append(res['answer'])
    context.append(' '.join([x.page_content for x in res['source_documents']]))

ml_suite.run('35_base', candidate_output_list=answers, context_list=context, model_name=MODEL_VERSION)

answers = []
context = []
for paper in climate_suite.suite.test_cases:
    res = climate_qa(paper.input)
    answers.append(res['answer'])
    context.append(' '.join([x.page_content for x in res['source_documents']]))

climate_suite.run('35_base', candidate_output_list=answers, context_list=context, model_name=MODEL_VERSION)


ml_paper = get_model(MODEL_VERSION_TO_PROMOTE, 'ml_papers_index')
climate_qa = get_model(MODEL_VERSION_TO_PROMOTE, 'climate_index')

answers = []
context = []
for paper in ml_suite.suite.test_cases:
    res = ml_paper(paper.input)
    answers.append(res['answer'])
    context.append(' '.join([x.page_content for x in res['source_documents']]))

ml_suite.run('35_upgrade', candidate_output_list=answers, context_list=context, model_name=MODEL_VERSION_TO_PROMOTE)

answers = []
context = []
for paper in climate_suite.suite.test_cases:
    res = climate_qa(paper.input)
    answers.append(res['answer'])
    context.append(' '.join([x.page_content for x in res['source_documents']]))

climate_suite.run('35_upgrade', candidate_output_list=answers, context_list=context, model_name=MODEL_VERSION_TO_PROMOTE)