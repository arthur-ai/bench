from pydantic import BaseModel


class HallucinationScoreRequest(BaseModel):
    """
    Request for hallucination classification
    """

    user_input: str
    """
    User input with which to determine if the model generated response is supported
    """

    context: str
    """
    Context with which to determine if the model generated response is supported
    """

    response: str
    """
    Model generated response
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
