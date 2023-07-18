from datasets import load_metric
from typing import List, Optional
from arthur_bench.scoring import ScoringMethod

class CodeEval(ScoringMethod):
    """
    Wrapping the HuggingFace code_eval metric
    
    https://huggingface.co/spaces/evaluate-metric/code_eval
    """
    def __init__(self):
        self.scorer = load_metric("code_eval") # type: ignore

    def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        
        res = []
        for i in range(len(candidate_batch)):
            pass_at_k, _ = self.scorer.compute(references=[reference_batch[i]], predictions=[[candidate_batch[i]]])
            res.append(pass_at_k['pass@1'])
        return res
    