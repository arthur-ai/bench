# flake8: noqa

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_message_prompt = SystemMessagePromptTemplate.from_template(
    """You compare two summaries of a text. You respond with a Choice, either a 0, 1, or tie ONLY.
(0 = response 0 is better, 1 = response 1 is better, tie = no significant difference between the responses).
A good summary captures the most important information in the text and doesnt focus too much on small details.
A bad summary has information that is conflicting or irrelevant to the original text, or has typos of words in the text."""
)
example_summaries_1 = HumanMessagePromptTemplate.from_template(
    """Text: (The Hollywood Reporter)Add another fan-favorite
character to the cast of next year's X-Men: Apocalypse, with director Bryan Singer announcing
 via Instagram that Olivia Munn will play the telepathic Psylocke in the follow-up to X-Men:
Days of Future Past. Singer revealed that the Newsroom actress would play Betsy Braddock in
the movie (presumably before the confusing and complicated plot twist that saw Psylocke
change from a Caucasian former supermodel to a Japanese ninja for no immediately obvious
reason).
Response 0:
Bryan Singer said that he would love to see Olivio Mun in x-men: apocalypse. 
Response 1:
Bryan Singer has revealed that Olivia Munn will star as Psylocke in next year's x-men:
apocalypse - a character created more than 20 years ago for the x-men.
Choice:"""
)
example_choice_1 = AIMessagePromptTemplate.from_template("1")
example_summaries_2 = HumanMessagePromptTemplate.from_template(
    """Text: (The Hollywood Reporter)Add another fan-favorite
character to the cast of next year's X-Men: Apocalypse, with director Bryan Singer announcing
 via Instagram that Olivia Munn will play the telepathic Psylocke in the follow-up to X-Men:
Days of Future Past. Singer revealed that the Newsroom actress would play Betsy Braddock in
the movie (presumably before the confusing and complicated plot twist that saw Psylocke
change from a Caucasian former supermodel to a Japanese ninja for no immediately obvious
reason).
Response 0:
Bryan Singer announced Olivia Munn will lead as the classic character Psylocke in the upcoming movie X-Men: Apocalypse
Response 1:
Bryan Singer has revealed that Olivia Munn will star as Psylocke in next year's x-men:
apocalypse - a character created more than 20 years ago for the x-men.
Choice:"""
)
example_choice_2 = AIMessagePromptTemplate.from_template("tie")
comparison_template = HumanMessagePromptTemplate.from_template(
    """Text: {text}
Response 0: {summary_A}
Response 1: {summary_B}
Choice:"""
)

COMPARE = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        example_summaries_1,
        example_choice_1,
        example_summaries_2,
        example_choice_2,
        comparison_template,
    ]
)
