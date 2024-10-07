import pandas as pd
from langchain_openai import ChatOpenAI
from langchain import (
    OpenAI,
    PromptTemplate,
    LLMChain,
)
from langchain_experimental.agents import create_pandas_dataframe_agent
# from langchain_experimental import summarize


def get_agent(df: pd.DataFrame):
    llm = ChatOpenAI()
    return create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)


def ask_question(question: str, df: pd.DataFrame) -> str:
    try:
        agent = get_agent(df=df)
        answer = agent.run(question)

        if isinstance(answer, dict):
            return answer.get("output", "No Answer")
        if isinstance(answer, str):
            return answer

    except Exception as e:
        print(f"Exception: {e}")
    return "No Answer"

def summarize_website(url: str) -> str:
    template = """
    You are a helpful assistant. Please summarize the patent published on the following website:

    {url}
    """

    llm = OpenAI()
    prompt = PromptTemplate(template=template, input_variables=["url"])
    chain = LLMChain(prompt=prompt, llm=llm)

    summary = chain.run(url=url)
    return summary


def summarize_text(text: str) -> str:
    template = """
    You are a helpful assistant. Please summarize the following text:

    {text}
    """

    llm = OpenAI()
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = LLMChain(prompt=prompt, llm=llm)

    summary = chain.run(text=text)
    return summary
