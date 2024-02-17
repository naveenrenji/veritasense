# from stageOne.get_answer import get_answer
# from stageTwo.SSEmodel import get_SSE_results
# from stageThree.responseGeneratorOpenAI import response_generator
# from time import time


# def get_bot_response(query):
#     t=time()
#     context = get_answer(query)
#     # If the response was '', there was no match at stage 1, hence -> stage 2 component
#     if context == 'not found':
#         context = get_SSE_results(query)  # Implement your model function here
#         print(context) # for debugging only
#         #pass  # Placeholder for stage 2 component

#     # Now we pass the data to the stage 3 component. 
#     if context == 'not found':
#         response = "Sorry, I do not have the answer to that, please ask me another question."
#     else: 
#         response = response_generator(query, context)
#     print('Total time:', round(time() - t, 4), 'seconds')
#     return response

def get_bot_response(query):
    return "mock"


#print(get_bot_response("what version of python are we using in class?"))

