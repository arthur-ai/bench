import requests
from typing import List, Optional
from arthur_bench.scoring import ScoringMethod

HALLUCINATION_CHECK_API = "https://dnx8z19dub.execute-api.us-east-2.amazonaws.com/prod/hello"


class Hallucination(ScoringMethod):

    @staticmethod
    def name() -> str:
        return "hallucination"

    def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        res = []
        for i in range(len(candidate_batch)):
            response = requests.get(HALLUCINATION_CHECK_API)
            if response.status_code == 200:
                data = response.json()
                res.append(float(data["hallucination"]))
                print(data["reason"])
            else:
                res.append(-1.0)
        return res