import os

from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import create_structured_output_chain

from structure_classes import Report


def run_model(transcript, contexts):
    os.environ['OPENAI_API_KEY'] = os.getenv('OPEN_AI_KEY')

    sys_template = """
                        You are an expert analyst of software accessibility, usability and UI, UX.
                        You will be provided with a transcript of a user study, where a user with disability is testing the accessibility of a software application.
                        Your job is to parse through the transcript, and detect the accessibilty and usability issues reported.
                        There can be cases where the tester reports no issues or provides positive feedback. Do not mention such cases in the report.
                        Do not forcibly detect an issue where there is none. Only report one if it is apparent.
                        
                        {contexts}                 
                    """

    human_template = """
                        Currently, the transcript is formatted as a list of speeches with timestamps.
                        The current format is: <start time> --> <end time> <speaker>: <text>
                        Example: 00:09:22.330 --> 00:09:24.699 Joe: How are you?

                        List out the timestamps i.e. <start time> --> <end time> in the output to refer to where in the transcript the issue was reported.
                        
                        Here's the transcript
                        {transcript}
                    """

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", sys_template),
        ("human", human_template),
    ])

    llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0)

    # chain = LLMChain(llm=llm, prompt=chat_prompt, verbose=True, output_key='findings')
    chain = create_structured_output_chain(Report, llm, chat_prompt, verbose=True)

    with get_openai_callback() as cb:
        result = chain.run({
            "contexts": contexts,
            "transcript": transcript
        })
    total_tokens = cb.total_tokens
    print(f"TOTAL TOKENS: {total_tokens}")

    return total_tokens, result
