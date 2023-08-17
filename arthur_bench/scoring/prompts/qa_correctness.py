# flake8: noqa

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_message_prompt = SystemMessagePromptTemplate.from_template(
    """Given the following context (extracted parts of a long document), a question, and an answer, decide if the final answer is correct.
You respond with a decision, either a 0, 1, or NA ONLY.
(0 = answer is incorrect, 1 = answer is correct, NA = you do not know. Don't try to make up an answer.).
If the question is not discussed in the provided context and the Answer says that the question is not discussed in the provided context, mark it as correct.
A correct answer is in accordance with fact and truth, answers the question posed, and is supported by the evidence found in the extracted parts of the context documents.
An incorrect answer has information that is conflicting or irrelevant to the extracted parts of the context documents, or has typos of words in the text,
or is a factually incorrect response to the questions."""
)
example_summaries_1 = HumanMessagePromptTemplate.from_template(
    """QUESTION: Compounds that are capable of accepting electrons, such as o 2 or f2, are called what?
========
CONTEXT: Oxidants and Reductants Compounds that are capable of accepting electrons, such as O 2 or F2, are called oxidants (or oxidizing agents) because they can oxidize other compounds. 
In the process of accepting electrons, an oxidant is reduced. Compounds that are capable of donating electrons, such as sodium metal or cyclohexane (C6H12), are called 
reductants (or reducing agents) because they can cause the reduction of another compound. In the process of donating electrons, a reductant is oxidized. These relationships are 
summarized in Equation 3.30: Equation 3.30 Saylor URL: http://www. saylor. org/books.
========
ANSWER: oxidants
DECISION:"""
)
example_choice_1 = AIMessagePromptTemplate.from_template("1")
example_summaries_2 = HumanMessagePromptTemplate.from_template(
    """QUESTION: What term in biotechnology means a genetically exact copy of an organism?
========
CONTEXT: But transgenic animals just have one novel gene. What about an animal with a whole new genome? Could a clone , a genetically exact copy of an organism, be 
developed using techniques associated with biotechnology? It could be argued that human cloning is one of the inevitable 
outcomes of modern biotechnology. It "simply" involves the removal of the nucleus from a somatic cell and its placement into an unfertilized egg cell whose nucleus has 
either been deactivated or removed. This new cell would mimic the zygote, the first diploid cell of a new organism. This new zygote is allowed to become established, 
and a few days later is placed into the uterus of a surrogate mother. Theoretically this would result in an individual genetically identical to the donor. Obviously, 
there are many ethical and legal issues associated with human cloning, and of course, it is not a "simple" procedure. But animal cloning is arguably a different story.
========
ANSWER: genome
DECISION:"""
)
example_choice_2 = AIMessagePromptTemplate.from_template("0")
example_summaries_3 = HumanMessagePromptTemplate.from_template(
    """QUESTION: What is the a mountain range in California?
========
CONTEXT: As you know, the surface of Earth is not flat. Some places are high, and some places are low. For example, mountain ranges like the Sierra Nevada in California 
or the Andes in South America are high above the surrounding areas. An accurate location must take into account the third dimension. Elevation is the height above or 
below sea level. Sea level refers to the height of the ocean’s surface. This is the midpoint between high and low tide. Sea level can vary from place to place, but scientists 
base their elevation measurements on the average, or mean, sea level to make sure they have a standard reference point.
========
ANSWER: Adirondacks
DECISION:"""
)
example_choice_3 = AIMessagePromptTemplate.from_template("0")
comparison_template = HumanMessagePromptTemplate.from_template(
    """Given the following context (extracted parts of a long document), a question, and an answer, decide if the final answer is correct.
You respond with a decision, either a 0, 1, or NA ONLY.
(0 = answer is incorrect, 1 = answer is correct, NA = you do not know. Don't try to make up an answer.).
If the question is not discussed in the provided context and the Answer says that the question is not discussed in the provided context, mark it as correct.
A correct answer is in accordance with fact and truth, and is supported by the evidence found in the extracted parts of the context documents.
An incorrect answer has information that is conflicting or irrelevant to the extracted parts of the context documents, or has typos of words in the text, or is a factually incorrect response to the questions.
QUESTION: {question}
========
CONTEXT: {context}
========
ANSWER: {answer}
DECISION:"""
)

DECIDE = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        example_summaries_1,
        example_choice_1,
        example_summaries_2,
        example_choice_2,
        example_summaries_3,
        example_choice_3,
        comparison_template,
    ]
)
