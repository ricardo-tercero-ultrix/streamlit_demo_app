from langchain_utils import ask_question
from patents import PatentsHandler

file_name = "/data/streampatents-5000.csv"

handler = PatentsHandler(file_path=file_name)

df = handler.df

question = "How many patents were published on 2010"
ask_question(df=df, question=question)
