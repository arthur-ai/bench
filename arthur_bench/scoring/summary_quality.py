from enum import Enum
import logging
import json
import openai
from pydantic import BaseModel
from typing import List, Optional

from arthur_bench.scoring import ScoringMethod
from arthur_bench.client.exceptions import UserValueError

class SummaryComparisonResult(Enum):
    OPTION_0_BETTER = 0.0
    OPTION_1_BETTER = 1.0
    TIE = 0.5

class SummaryComparison(BaseModel):
    """The result of a summary comparison, returning a SummaryComparisonResult enum
    The comparison should be OPTION_0_BETTER if the summary labelled 0 is the better summary.
    The comparison should be OPTION_1_BETTER if the summary labelled 1 is the better summary.
    The comparison should be TIE if no summary is clearly better than the other.
    A good summary captures the most important information in the text and doesnt focus too much on small details.
    A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text.
    """
    comparison: SummaryComparisonResult
    
def compare_summaries(input_text: str, summary_0: str, summary_1: str):
    """Uses chatgpt to compare summaries"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        functions=[{
            'name': 'SummaryComparison',
            'description': 'The result of a summary comparison, returning a SummaryComparisonResult enum\n    The comparison should be OPTION_0_BETTER if the summary labelled 0 is the better summary.\n    The comparison should be OPTION_1_BETTER if the summary labelled 1 is the better summary.\n    The comparison should be TIE if no summary is clearly better than the other.\n    A good summary captures the most important information in the text and doesnt focus too much on small details.\n    A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text.\n    ',
            'parameters': {
                 '$defs': {'SummaryComparisonResult': {'enum': [0.0, 1.0, 0.5],
            'type': 'number'}},
            'properties': {'comparison': {'$ref': '#/$defs/SummaryComparisonResult'}},
            'required': ['comparison'],
            'type': 'object'}}],
        messages=[
            {"role": "system", "content": "I'm going to ask for the better summary of the input_text between two options. Use SummaryComparison.openai_schema to parse this data"},
            {"role": "user", "content": """
            Text: (The Hollywood Reporter)Add another fan-favorite
            character to the cast of next year's X-Men: Apocalypse, with director Bryan Singer announcing
            via Instagram that Olivia Munn will play the telepathic Psylocke in the follow-up to X-Men:
            Days of Future Past. Singer revealed that the Newsroom actress would play Betsy Braddock in
            the movie (presumably before the confusing and complicated plot twist that saw Psylocke
            change from a Caucasian former supermodel to a Japanese ninja for no immediately obvious
            reason).
            ===
            Summary 0:
            Bryan Singer said that he would love to see Olivio Mun in x-men: apocalypse. 
            ===
            Summary 1:
            Bryan Singer has revealed that Olivia Munn will star as Psylocke in next year's x-men:
            apocalypse - a character created more than 20 years ago for the x-men.
            ===
            Choice:
            """},
            {"role": "assistant", "content" : "", "function_call": {"name" : "SummaryComparison", "arguments" : "{\n  \"comparison\": 1.0\n}"}},
            {"role": "user", "content": """
            Text: (The Hollywood Reporter)Add another fan-favorite
            character to the cast of next year's X-Men: Apocalypse, with director Bryan Singer announcing
             via Instagram that Olivia Munn will play the telepathic Psylocke in the follow-up to X-Men:
            Days of Future Past. Singer revealed that the Newsroom actress would play Betsy Braddock in
            the movie (presumably before the confusing and complicated plot twist that saw Psylocke
            change from a Caucasian former supermodel to a Japanese ninja for no immediately obvious
            reason).
            ===
            Summary 0:
            Bryan Singer announced Olivia Munn will lead as the classic character Psylocke in the upcoming movie X-Men: Apocalypse
            ===
            Summary 1:
            Bryan Singer has revealed that Olivia Munn will star as Psylocke in next year's x-men:
            apocalypse - a character created more than 20 years ago for the x-men.
            ===
            Choice:
            """},
            {"role": "assistant", "content" : "", "function_call": {"name" : "SummaryComparison", "arguments" : "{\n  \"comparison\": 0.5\n}"}},
            {"role": "user", "content": f"""
            Text: {input_text}
            ========
            Summary 0: {summary_0}
            ========
            Summary 1: {summary_1}
            Choice:
            """}
        ],
    )
    completion_json = json.loads(completion['choices'][0]['message']['function_call']['arguments'])
    return SummaryComparison(**completion_json).comparison.value


CONTEXT_WINDOW = 2500
MAX_RETRIES = 5

class SummaryQuality(ScoringMethod):
	"""
	Comprehensive measure of summarization quality compared to a reference summary.
	"""

	def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
				  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
		"""
		Summary quality requires input_text_batch.
		"""
		if input_text_batch is None:
			raise UserValueError("input text is required for this scoring method. Please provide a dataframe column or a list of your input text strings in the Test Suite.")
		
		if context_batch is not None:
			raise UserValueError("using context is not currently supported for summary quality")
    
		res = []
		for i in range(len(input_text_batch)):
			# run LLMChain to choose whether summary A or summary B is a better summary of the input text
			# (on truncated input text to fit in ChatGPT context window)
			llm_input = input_text_batch[i][:CONTEXT_WINDOW]
			if llm_input != input_text_batch[i]:
				logging.warn("The input text has been truncated to fit in the LLM evaluator's context window")


			num_retries = 0
			while num_retries < MAX_RETRIES:
				try:
					choice = compare_summaries(llm_input, reference_batch[i], candidate_batch[i])
					break
				except ValueError:
					num_retries += 1
				if num_retries == MAX_RETRIES:
					raise SystemError(
					f"max retries attempted attempted to compare summaries: {input_text_batch[i]} {reference_batch[i]} {candidate_batch[i]}"
				)
			choice = compare_summaries(llm_input, reference_batch[i], candidate_batch[i])
			res.append(choice)

		return res


