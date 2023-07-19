import logging
import tiktoken
from typing import List, Optional, Tuple
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate, \
    HumanMessagePromptTemplate, BasePromptTemplate
from arthur_bench.scoring import ScoringMethod
from arthur_bench.client.exceptions import UserValueError

system_message_prompt = SystemMessagePromptTemplate.from_template(
"""You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY.
(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses).
A good summary captures the most important information in the text and doesnt focus too much on small details.
A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text."""
)
example_summaries_1 = HumanMessagePromptTemplate.from_template(
"""You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY.
(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses).
A good summary captures the most important information in the text and doesnt focus too much on small details.
A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text.
Text: (The Hollywood Reporter)Add another fan-favorite
character to the cast of next year's X-Men: Apocalypse, with director Bryan Singer announcing
 via Instagram that Olivia Munn will play the telepathic Psylocke in the follow-up to X-Men:
Days of Future Past. Singer revealed that the Newsroom actress would play Betsy Braddock in
the movie (presumably before the confusing and complicated plot twist that saw Psylocke
change from a Caucasian former supermodel to a Japanese ninja for no immediately obvious
reason).
Response 0:
Bryan Singer said that he would love to see Olivio Mun in x-men: apocalypse. 
Response 1:
Bryan Singer has revealed that Olivia Munn will star as Psylocke in next year's x-men:
apocalypse - a character created more than 20 years ago for the x-men.
Choice:"""
)
example_choice_1 = AIMessagePromptTemplate.from_template("1")
example_summaries_2 = HumanMessagePromptTemplate.from_template(
"""You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY.
(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses).
A good summary captures the most important information in the text and doesnt focus too much on small details.
A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text.
Text: (The Hollywood Reporter)Add another fan-favorite
character to the cast of next year's X-Men: Apocalypse, with director Bryan Singer announcing
 via Instagram that Olivia Munn will play the telepathic Psylocke in the follow-up to X-Men:
Days of Future Past. Singer revealed that the Newsroom actress would play Betsy Braddock in
the movie (presumably before the confusing and complicated plot twist that saw Psylocke
change from a Caucasian former supermodel to a Japanese ninja for no immediately obvious
reason).
Response 0:
Bryan Singer announced Olivia Munn will lead as the classic character Psylocke in the upcoming movie X-Men: Apocalypse
Response 1:
Bryan Singer has revealed that Olivia Munn will star as Psylocke in next year's x-men:
apocalypse - a character created more than 20 years ago for the x-men.
Choice:"""
)
example_choice_2 = AIMessagePromptTemplate.from_template("tie")
comparison_template = HumanMessagePromptTemplate.from_template(
"""You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY.
(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses).
A good summary captures the most important information in the text and doesnt focus too much on small details.
A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text.
Text: {text}
Response 0: {summary_A}
Response 1: {summary_B}
Choice:"""
)

COMPARE = ChatPromptTemplate.from_messages(
    [system_message_prompt, example_summaries_1, example_choice_1, example_summaries_2, example_choice_2,
     comparison_template])

CONTEXT_WINDOW_MAP = {
	'gpt-3.5-turbo' : 4096,
	'gpt-4' : 8192,
	'gpt-3.5-turbo-16k' : 16384,
	'gpt-4-32k' : 32768
}
EVALUATOR_MODEL = 'gpt-3.5-turbo'
TIKTOKEN_ENCODER = tiktoken.get_encoding("cl100k_base")
LLM_CHOICE_OPTIONS = {'0': 0.0, '1': 1.0, 'tie': 0.5}


logger = logging.getLogger(__name__)

def truncate_input_text(input_text, ref_output, cand_output) -> Tuple[str, bool]:
    """Truncates the input_text to fit in LLM evaluator context
    
    Truncate the input text so that the filled-in COMPARE prompt
    which contains {input text + summary A + summary B} fits in the evaluator context window
    
    Returns the tuple (text, whether text was truncated)
    """
    llm_prompt_untruncated = COMPARE.format(text=input_text, summary_A=ref_output, summary_B=cand_output)
    llm_prompt_tokens = TIKTOKEN_ENCODER.encode(llm_prompt_untruncated)
    num_to_truncate_from_input_text_tokens = len(llm_prompt_tokens) - CONTEXT_WINDOW_MAP[EVALUATOR_MODEL]
    truncated = False
    if num_to_truncate_from_input_text_tokens > 0:
        input_text_tokens_truncated = input_text_tokens_truncated[:-num_to_truncate_from_input_text_tokens]
        input_text = TIKTOKEN_ENCODER.decode(input_text_tokens_truncated)
        truncated = True
    return input_text, truncated


class SummaryQuality(ScoringMethod):
    """
    Comprehensive measure of summarization quality compared to a reference summary.
    """

    def __init__(self):
        self.summary_compare = LLMChain(llm=ChatOpenAI(temperature=0), prompt=COMPARE)  # type: ignore

    def run(self, inputs: List[str], reference_outputs: List[str], candidate_outputs: List[str],
            contexts: List[str], batch_size: int) -> list:
        # truncate inputs if needed
        truncated_inputs = []
        num_truncated = 0
        for i, inp in enumerate(inputs):
            inp, truncated = truncate_input_text(inp, reference_outputs[i], candidate_outputs[i])
            num_truncated += int(truncated)

            # add to list we'll actually use
            truncated_inputs.append(inp)

        if num_truncated > 0:
            logger.warning(f"Truncated {num_truncated} out of {len(inputs)} total summary inputs to "
                           f"{CONTEXT_WINDOW_MAP[EVALUATOR_MODEL]} characters")

        return super().run(truncated_inputs, reference_outputs, candidate_outputs, contexts, batch_size)

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
            
            choice = self.summary_compare({"text": input_text_batch[i], "summary_A": reference_batch[i],
                                           "summary_B": candidate_batch[i]})

            # return -1.0 if the LLMChain returns an invalid result
            if "text" in choice:
                res.append(LLM_CHOICE_OPTIONS.get(choice["text"][:3], -1.0))
            else:
                res.append(-1.0)
                
        return res
