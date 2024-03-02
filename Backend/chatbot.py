import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch._utils")

from stageOne.getcontext import get_answer, load_data
from stageTwo.dataloading import get_SSE_results, load_model_and_data
from stageThree.responseGenerator import response_generator
from time import time


# Initialize global variables to None
stageOneModel = None
question_embeddings = None
questions = None
df = None
stageTwoModel = None
corpus_sentences = None
corpus_embeddings = None

def get_bot_response(query):
    print("started")
    t=time()
    # Load data for stage one only if it hasn't been loaded before
    if stageOneModel is None or question_embeddings is None or questions is None or df is None:
        stageOneModel, question_embeddings, questions, df = load_data()
    context = get_answer(query, stageOneModel, question_embeddings, questions, df)
    print("stage 1 done")

    # If the response was '', there was no match at stage 1, hence -> stage 2 component
    if context == 'not found':
        if stageTwoModel is None or corpus_sentences is None or corpus_embeddings is None:
            stageTwoModel, corpus_sentences, corpus_embeddings = load_model_and_data()
        context = get_SSE_results(query, stageTwoModel, corpus_sentences, corpus_embeddings)  # Implement your model function here
        print(context) # for debugging only
        pass  # Placeholder for stage 2 component

    # Now we pass the data to the stage 3 component. 
    if context == 'not found':
        response = "Sorry, I do not have the answer to that, please ask me another question."
    else: 
        response = response_generator(query, context)
        # response = "Temporary response data -- " + context

    print("started response generation")
    print('Total time:', round(time() - t, 4), 'seconds')
    return response

# for debugging only
# def get_bot_response(query):
#     return "mock"


# print(get_bot_response("what version of python are we using in class?"))

# get_bot_response("what version of python are we using in class?")
