from pydantic import BaseModel

class HallucinationScoreRequest(BaseModel):
    response: str
    context: str

class HallucinationScoreResponse(BaseModel):
    hallucination: bool
    reason: str
