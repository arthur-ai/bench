from enum import Enum
from typing import List, Optional
import json
import openai
from openai_function_call import openai_schema
from pydantic import BaseModel

from arthur_bench.scoring import ScoringMethod
from arthur_bench.client.exceptions import UserValueError

class QA_ValidationResult(Enum):
    INCORRECT = 0.0
    CORRECT = 1.0
    UNCLEAR = -1.0

@openai_schema
class QA_Validation(BaseModel):
    """The result of question-answer validation, returning a QA_ValidationResult enum
    The validation should be INCORRECT if the answer to the question is wrong and/or unsupported by the context
    The validation should be CORRECT if the answer to the question is correct and/or supported by the context.
    A correct answer is in accordance with fact and truth, answers the question posed, and is supported by the evidence found in the extracted parts of the context documents.
    An incorrect answer has information that is conflicting or irrelevant to the extracted parts of the context documents, or has typos of words in the text,
or is a factually incorrect response to the questions.
    """
    validation: QA_ValidationResult
        
def validate_question_answer(question: str, answer: str, context: str):
    """Uses chatgpt to evaluate whether the answer to a question, given a context, is incorrect"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        functions=[QA_Validation.openai_schema],
        messages=[
            {"role": "system", "content": "I'm going to ask for the answer to a question to be validated against its context. Use QA_Validation.openai_schema to parse this data"},
            {"role": "user", "content": """
            QUESTION: Compounds that are capable of accepting electrons, such as o 2 or f2, are called what?
            ========
            CONTEXT: Oxidants and Reductants Compounds that are capable of accepting electrons, such as O 2 or F2, are called oxidants (or oxidizing agents) because they can oxidize other compounds. 
            In the process of accepting electrons, an oxidant is reduced. Compounds that are capable of donating electrons, such as sodium metal or cyclohexane (C6H12), are called 
            reductants (or reducing agents) because they can cause the reduction of another compound. In the process of donating electrons, a reductant is oxidized. These relationships are 
            summarized in Equation 3.30: Equation 3.30 Saylor URL: http://www. saylor. org/books.
            ========
            ANSWER: oxidants
            DECISION:
            """},
            {"role": "assistant", "content" : "", "function_call": {"name" : "QA_Validation", "arguments" : "{\n  \"validation\": 1.0\n}"}},
            {"role": "user", "content": """
            QUESTION: What term in biotechnology means a genetically exact copy of an organism?
            ========
            CONTEXT: But transgenic animals just have one novel gene. What about an animal with a whole new genome? Could a clone , a genetically exact copy of an organism, be 
            developed using techniques associated with biotechnology? It could be argued that human cloning is one of the inevitable 
            outcomes of modern biotechnology. It "simply" involves the removal of the nucleus from a somatic cell and its placement into an unfertilized egg cell whose nucleus has 
            either been deactivated or removed. This new cell would mimic the zygote, the first diploid cell of a new organism. This new zygote is allowed to become established, 
            and a few days later is placed into the uterus of a surrogate mother. Theoretically this would result in an individual genetically identical to the donor. Obviously, 
            there are many ethical and legal issues associated with human cloning, and of course, it is not a "simple" procedure. But animal cloning is arguably a different story.
            ========
            ANSWER: genome
            DECISION:
            """},
            {"role": "assistant", "content" : "", "function_call": {"name" : "QA_Validation", "arguments" : "{\n  \"validation\": 0.0\n}"}},
            {"role": "user", "content": """
            QUESTION: What is the a mountain range in California?
            ========
            CONTEXT: As you know, the surface of Earth is not flat. Some places are high, and some places are low. For example, mountain ranges like the Sierra Nevada in California 
            or the Andes in South America are high above the surrounding areas. An accurate location must take into account the third dimension. Elevation is the height above or 
            below sea level. Sea level refers to the height of the ocean’s surface. This is the midpoint between high and low tide. Sea level can vary from place to place, but scientists 
            base their elevation measurements on the average, or mean, sea level to make sure they have a standard reference point.
            ========
            ANSWER: Adirondacks
            DECISION:
            """},
            {"role": "assistant", "content" : "", "function_call": {"name" : "QA_Validation", "arguments" : "{\n  \"validation\": 0.0\n}"}},
            {"role": "user", "content": f"""
            QUESTION: {question}
            ========
            CONTEXT: {context}
            ========
            ANSWER: {answer}
            DECISION:
            """}
        ],
    )
    completion_json = json.loads(completion['choices'][0]['message']['function_call']['arguments'])
    return QA_Validation(**completion_json).validation.value


MAX_RETRIES = 5


class QAQualityCorrectness(ScoringMethod):
    """
    Given an input question, context string, and model generation, determine if the generation produced a correct answer.
    """

    def run_batch(self, reference_batch: List[str], candidate_batch: List[str], input_text_batch: Optional[List[str]] = None, 
                  context_batch: Optional[List[str]] = None) -> List[float]:
      """
      Reference batch is not used for this scoring method, QA correctness requires an input_text_batch and context_batch
      """
      if input_text_batch is None:
        raise UserValueError("input text is required for this scoring method. Please provide a dataframe column or a list of your input text strings in the Test Suite.")
      if context_batch is None:
        raise UserValueError("context is required for this scoring method. Please provide a dataframe column or a list of your context strings in the Test Suite.")
      
      res = []
      for i in range(len(input_text_batch)):
        num_retries = 0
        while num_retries < MAX_RETRIES:
          try:
            llmchoice = validate_question_answer(input_text_batch[i], candidate_batch[i], context_batch[i])
            break
          except ValueError:
            num_retries += 1
        if num_retries == MAX_RETRIES:
            raise SystemError(
              f"max retries attempted attempted to validate question-answer: {input_text_batch[i]} {candidate_batch[i]} {context_batch[i]}"
          )
        res.append(llmchoice)
      return res
