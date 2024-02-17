import openai

openai.api_key = "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"
conversation_history = []

def response_generator(question, context):
    global conversation_history
    
    conversation_history.append({
        "role": "user",
        "content": f"Question: {question}\nContext: {context}"
    })

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    system_message = {
        "role": "system",
        "content": "You are a professor who loves his students and is very empathetic, wise, and knowledgeable. You will respond only with information given in the context or the chat history, whichever is relevant, but respond directly to the query without mentioning the context. If the context is empty, you will say that you do not know the answer to that yet. Do not hallucinate and give extra information."
    }
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[system_message] + conversation_history,
        temperature=1,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    
    # Extract the response text
    response_text = response['choices'][0]['message']['content'].strip()
    
    # Append the model's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": response_text
    })

    # Ensure that only the last 5 messages are kept after the response is added
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    return response_text

# Example usage:
#question = "Who is Naveen?"
#context = "Naveen is a graduate student at Stevens Institute of Technology who is very interested in AI. Naveen is from Bahrain, a small island in the Middle East but his homeland is Kerala, India"

#print(response_generator(question, context))
