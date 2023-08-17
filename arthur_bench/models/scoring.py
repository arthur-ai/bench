from pydantic import BaseModel


class HallucinationScoreRequest(BaseModel):
    """
    Request for hallucination classification
    """

    response: str
    """
    Model generated response
    """
    context: str
    """
    Context with which to determine if the model generated response is supported
    """


class HallucinationScoreResponse(BaseModel):
    """
    Hallucination classification
    """

    hallucination: bool
    """
    True if hallucination, false otherwise
    """
    reason: str
    """
    Justification for the hallucination classification
    """
