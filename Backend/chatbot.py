from stageOne.getcontext import get_answer
from stageOne.getcontext import load_data
from stageTwo.dataloading import get_SSE_results
from stageTwo.dataloading import load_model_and_data
from stageTwo.SSEmodel import get_SSE_results
from stageThree.responseGenerator import response_generator
from time import time


def get_bot_response(query):
    t=time()
    model, question_embeddings, questions, df = load_data()
    context = get_answer(query, model, question_embeddings, questions, df)
    # If the response was '', there was no match at stage 1, hence -> stage 2 component
    if context == 'not found':
        sseModel, corpus_sentences, corpus_embeddings = load_model_and_data()
        context = get_SSE_results(query, sseModel, corpus_sentences, corpus_embeddings)  # Implement your model function here
        print(context) # for debugging only
        pass  # Placeholder for stage 2 component

    # Now we pass the data to the stage 3 component. 
    if context == 'not found':
        response = "Sorry, I do not have the answer to that, please ask me another question."
    else: 
        response = response_generator(query, context)
    #     #response = "Temporary response data -- " + context
    # print("started response generation")
    # response = response_generator(query, "My name is naveen")
    print('Total time:', round(time() - t, 4), 'seconds')
    return response

# for debugging only
# def get_bot_response(query):
#     return "mock"


# print(get_bot_response("what version of python are we using in class?"))

# get_bot_response("what version of python are we using in class?")
