from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import os
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question: {question}")
    ]
)

# Ollama Llama2 LLM
llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Terminal interface
while True:
    input_text = input("Enter the topic you want to ask about: ")
    if input_text.lower() == 'exit':
        break
    response = chain.invoke({"question": input_text})
    print("Response:", response)
