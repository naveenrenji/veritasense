import warnings
warnings.filterwarnings("ignore")

from stageOne.getcontext import get_answer, load_data
from stageTwo.getResponse import get_answer2, load_data2
# from stageTwo.dataloading import get_SSE_results, load_model_and_data
# from stageThree.gptneo import generate_response
from time import time


from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_experimental.chat_models import Llama2Chat

from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


template_messages = [
    SystemMessage(content="You are a compuer science professor."),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{text}"),
]
prompt_template = ChatPromptTemplate.from_messages(template_messages)

from langchain_community.llms import HuggingFaceTextGenInference

llm = HuggingFaceTextGenInference(
    inference_server_url="http://127.0.0.1:8080/",
    max_new_tokens=512,
    top_k=50,
    temperature=0.1,
    repetition_penalty=1.03,
)

model = Llama2Chat(llm=llm)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = LLMChain(llm=model, prompt=prompt_template, memory=memory)


# # Initialize global variables to None
# stageOneModel = None
# question_embeddings = None
# questions = None
# df = None
# stageTwoModel = None
# corpus_sentences = None
# corpus_embeddings = None
# loadedStageOneModel = False
# loadedStageTwoModel = False

def get_bot_response(query):
    print("started")
    t=time()
    # # Load data for stage one only if it hasn't been loaded before
    # if loadedStageOneModel is False:
    #     stageOneModel, question_embeddings, questions, df = load_data()
    #     loadedStageOneModel = True
    stageOneModel, question_embeddings, questions, df = load_data()
    context = get_answer(query, stageOneModel, question_embeddings, questions, df)
    print("stage 1 done")

    # If the response was '', there was no match at stage 1, hence -> stage 2 component
    if context == 'not found':
        # if loadedStageTwoModel is False:
        #     stageTwoModel, corpus_sentences, corpus_embeddings = load_model_and_data()
        #     loadedStageTwoModel = True
        # stageTwoModel, corpus_sentences, corpus_embeddings = load_model_and_data()
        # context = get_SSE_results(query, stageTwoModel, corpus_sentences, corpus_embeddings)  # Implement your model function here
        # print(context) # for debugging only
        # pass  # Placeholder for stage 2 component
        stageOneModel, question_embeddings, questions, df = load_data2()
        context = get_answer2(query, stageOneModel, question_embeddings, questions, df)
        print(context) # for debugging only

    # Now we pass the data to the stage 3 component. 
    # context = "python3.0 is the version we use in class"
    if context == 'not found':
        response = "Hello, please ask me a question related to Python Programming."
    else: 
        # print("this one")
        # print(query, context)
        prompt = f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {query}\nThis is the context to use - Context: {context}. now respond based on the context -"
        response = chain.run(text=prompt)
        
        # response = generate_response(query, context)
        # response = "Temporary response data -- " + context

    print("started response generation")
    print('Total time:', round(time() - t, 4), 'seconds')
    return response

# for debugging only
# def get_bot_response(query):
#     return "mock"


print(get_bot_response("what is object oriented programming?"))

print(get_bot_response("what version of python are we using in class?"))
