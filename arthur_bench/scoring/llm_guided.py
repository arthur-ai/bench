import re
import logging
from typing import List, Optional
from arthur_bench.models.config import EvaluatorConfig, Evaluator 
from arthur_bench.scoring.scoring_method import ScoringMethod


logger = logging.getLogger(__name__)

class LLMGuidedScorer(ScoringMethod):
    def __init__(self, 
                 evaluator_config: EvaluatorConfig,
                 ):
        self.evaluator = evaluator_config.to_evaluator()
        self.score_config = evaluator_config.score_config
        
    def to_float(self, resp: str) -> float:
        # first look for float score in resp
        score = re.findall(r"[-+]?(?:\d*\.*\d+)", resp)
        if len(score) == 1:
            return float(score[0])
        
        # look for known classifier strings
        score_keys = sorted(list(self.score_config.keys()), key = lambda x: len(x))
        for key in score_keys:
            if re.match(resp, key):
                return self.score_config[key]
        
        logger.warning("llm response could not be converted to float: {resp}")
        return -1.0 # TODO: this is throwing off avgs

    def run_batch(self, candidate_batch: List[str], reference_batch: Optional[List[str]] = None,
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        
        scores = []
        for i in range(len(candidate_batch)):
            resp = self.evaluator({"text": candidate_batch[i]})["text"]
            scores.append(self.to_float(resp))
        return scores


    