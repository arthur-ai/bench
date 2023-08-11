import re
import logging
from typing import List, Optional
from arthur_bench.models.config import LMConfig
from arthur_bench.scoring.scoring_method import ScoringMethod
from langchain.chains import LLMChain
from langchain import PromptTemplate


logger = logging.getLogger(__name__)


LLM_CHOICE_OPTIONS = {'0': 0.0, '1': 1.0, 'tie': 0.5, 'yes': 1.0, 'no': 0.0, 'correct': 1.0, 'incorrect': 0.0}


class LLMGuidedScorer(ScoringMethod):
    def __init__(self, 
                 evaluator_config: LMConfig, 
                 eval_prompt: str):
        model = evaluator_config.to_evaluator()
        self.evaluator = LLMChain(llm=model, 
                                  prompt=PromptTemplate.from_template(eval_prompt + "Text: {candidate} Score: "))
    
    @staticmethod
    def to_float(resp: str) -> float:
        # first look for float score in resp
        score = re.findall(r"[-+]?(?:\d*\.*\d+)", resp)
        if len(score) == 1:
            return float(score[0])
        
        # look for known classifier strings
        # TODO: use regex here
        if resp[:9] in LLM_CHOICE_OPTIONS:
            return LLM_CHOICE_OPTIONS[resp[:9]]
        
        logger.warning("llm response could not be converted to float: {resp}")
        return -1.0 # TODO: this is throwing off avgs

    def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None,
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        
        scores = []
        for i in range(len(candidate_batch)):
            resp = self.evaluator({"candidate": candidate_batch[i]})["text"]
            scores.append(LLMGuidedScorer.to_float(resp))
        return scores


    