import logging
from typing import List, Optional
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate, \
    HumanMessagePromptTemplate, BasePromptTemplate
from arthur_bench.scoring import ScoringMethod
from arthur_bench.client.exceptions import UserValueError

system_message_prompt = SystemMessagePromptTemplate.from_template(
    "You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY."
    "(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses). "
    "A good summary captures the most important information in the text and doesnt focus too much on small details."
    "A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text."
)
example_summaries_1 = HumanMessagePromptTemplate.from_template(
    "You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY."
    "(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses). "
    "A good summary captures the most important information in the text and doesnt focus too much on small details."
    "A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text."
    "Text: (The Hollywood Reporter)Add another fan-favorite "
    "character to the cast of next year's X-Men: Apocalypse, with director Bryan Singer announcing"
    " via Instagram that Olivia Munn will play the telepathic Psylocke in the follow-up to X-Men: "
    "Days of Future Past. Singer revealed that the Newsroom actress would play Betsy Braddock in "
    "the movie (presumably before the confusing and complicated plot twist that saw Psylocke "
    "change from a Caucasian former supermodel to a Japanese ninja for no immediately obvious "
    "reason)."
    "Response 0: "
    "Bryan Singer said that he would love to see Olivio Mun in x-men: apocalypse. "
    "Response 1: "
    "Bryan Singer has revealed that Olivia Munn will star as Psylocke in next year's x-men: "
    "apocalypse - a character created more than 20 years ago for the x-men. "
    "Choice: "
)
example_choice_1 = AIMessagePromptTemplate.from_template("1")
example_summaries_2 = HumanMessagePromptTemplate.from_template(
    "You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY."
    "(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses). "
    "A good summary captures the most important information in the text and doesnt focus too much on small details."
    "A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text."
    "Text: (The Hollywood Reporter)Add another fan-favorite "
    "character to the cast of next year's X-Men: Apocalypse, with director Bryan Singer announcing"
    " via Instagram that Olivia Munn will play the telepathic Psylocke in the follow-up to X-Men: "
    "Days of Future Past. Singer revealed that the Newsroom actress would play Betsy Braddock in "
    "the movie (presumably before the confusing and complicated plot twist that saw Psylocke "
    "change from a Caucasian former supermodel to a Japanese ninja for no immediately obvious "
    "reason)."
    "Response 0: "
    "Bryan Singer announced Olivia Munn will lead as the classic character Psylocke in the upcoming movie X-Men: Apocalypse"
    "Response 1: "
    "Bryan Singer has revealed that Olivia Munn will star as Psylocke in next year's x-men: "
    "apocalypse - a character created more than 20 years ago for the x-men. "
    "Choice: "
)
example_choice_2 = AIMessagePromptTemplate.from_template("tie")
comparison_template = HumanMessagePromptTemplate.from_template(
    "You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY."
    "(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses)."
    "A good summary captures the most important information in the text and doesnt focus too much on small details."
    "A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text."
    "Text: {text}"
    "Response 0: {summary_A}"
    "Response 1: {summary_B}"
    "Choice:"
)

COMPARE = ChatPromptTemplate.from_messages(
    [system_message_prompt, example_summaries_1, example_choice_1, example_summaries_2, example_choice_2,
     comparison_template])

CONTEXT_WINDOW = 2500
LLM_CHOICE_OPTIONS = {'0': 0.0, '1': 1.0, 'tie': 0.5}


class SummaryQuality(ScoringMethod):
    """
    Comprehensive measure of summarization quality compared to a reference summary.
    """

    def __init__(self):
        self.summary_compare = LLMChain(llm=ChatOpenAI(temperature=0), prompt=COMPARE)  # type: ignore

    def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
                  input_text_batch: Optional[List[str]] = None,
                  context_batch: Optional[List[str]] = None) -> List[float]:
        """
        Summary quality requires input_text_batch.
        """
        if input_text_batch is None:
            raise UserValueError(
                "input text is required for this scoring method. Please provide a dataframe column or a list of your "
                "input text strings in the Test Suite.")

        if context_batch is not None:
            raise UserValueError("using context is not currently supported for summary quality")

        res = []
        for i in range(len(input_text_batch)):
            # run LLMChain to choose whether summary A or summary B is a better summary of the input text
            # (on truncated input text to fit in ChatGPT context window)
            llm_input = input_text_batch[i][:CONTEXT_WINDOW]
            if llm_input != input_text_batch[i]:
                logging.warn("The input text has been truncated to fit in the LLM evaluator's context window")
            choice = self.summary_compare({"text": llm_input, "summary_A": reference_batch[i],
                                           "summary_B": candidate_batch[i]})

            # return -1.0 if the LLMChain returns an invalid result
            if "text" in choice:
                res.append(LLM_CHOICE_OPTIONS.get(choice["text"][:3], -1.0))
            else:
                res.append(-1.0)
        return res
