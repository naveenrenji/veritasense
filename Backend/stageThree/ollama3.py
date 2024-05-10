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
        ("system", "You are a helpful Python Programming assistant. Please respond to the user queries."),
        ("user", "Question: {question}")
    ]
)

# Setting up Ollama with Langchain
llm = Ollama(model="llama3")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Function to simulate chat using the last 5 messages as context
def chat(question):
    # Build context from the last 5 messages
    context = "\n".join(msg['content'] for msg in messages[-5:])
    full_prompt = f"Context: {context}\nQuestion: {question}"
    response = chain.invoke({"question": full_prompt})
    return response

# Function to manage the messages list and generate responses
def response_generator(question, context):
    combined_question = f"Based on the context, answer this question as a computer science Python Programming professor chatbot: {question}\nContext: {context}. Respond based on the context and your knowledge."
    response = chat(combined_question)
    # Store user's question and system's response, maintaining only the last 5 interactions
    messages.append({"role": "user", "content": question})
    messages.append({"role": "system", "content": response})
    # Keep only the last 5 messages for each role (10 messages total)
    if len(messages) > 10:
        messages.pop(0)  # Remove the oldest message first
        messages.pop(0)  # Continue removing to maintain length
    return response

# Terminal interface for interactive chat
# while True:
#     input_text = input("Enter the topic you want to ask about: ")
#     if input_text.lower() == 'exit':
#         break
#     context = "" 
#     response = response_generator(input_text, context)
#     print("Response:", response)


