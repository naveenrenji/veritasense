# Use a pipeline as a high-level helper
from transformers import pipeline


def response_generator(question, context):
    pipe = pipeline("question-answering", model="google/gemma-2b")
    response = pipe(question=question, context=context)
    return response['answer']

res = print(response_generator("tell me about myself", "My name is Naveen I am a boy forom bahrain and i love to play agmes with all my fiendds"))