import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = "llama3"  # TODO: update this for whatever model you wish to use
messages = []


def chat(messages):
    r = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = output
            return message


def response_generator(question, context):
    prompt = f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context as well as your own knowledge."
    messages.append({"role": "user", "content": prompt})
    message = chat(messages)
    messages.append(message)
    return message


while True:
    input_text = input("Enter the topic you want to ask about: ")
    if input_text.lower() == 'exit':
        break
    context = "" 
    response = response_generator(input_text, context)
    print("Response:", response)
