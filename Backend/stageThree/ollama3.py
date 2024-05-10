import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

load_dotenv()

# Initialize conversation history
messages = []

# Initialize the prompt for Langchain's Ollama model
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question: {question}")
    ]
)

# Setting up Ollama with Langchain
llm = Ollama(model="llama3")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Function to simulate chat
def chat(question):
    response = chain.invoke({"question": question})
    return response

# Function to add context to the questions and maintain a stateful conversation
def response_generator(question, context):
    combined_question = f"Based on the context, answer this question as a computer science professor chatbot: {question}\nContext: {context}. Respond based on the context and your knowledge."
    messages.append({"role": "user", "content": combined_question})
    message = chat(combined_question)
    messages.append({"role": "system", "content": message})
    return message

# Terminal interface for interactive chat
while True:
    input_text = input("Enter the topic you want to ask about: ")
    if input_text.lower() == 'exit':
        break
    context = "Provide any relevant context here"  # Update this as necessary or collect from user input
    response = response_generator(input_text, context)
    print("Response:", response)
