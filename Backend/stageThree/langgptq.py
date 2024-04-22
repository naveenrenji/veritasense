import torch
from langchain import HuggingFacePipeline, PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
from collections import deque

# Initialize the model and tokenizer
MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto"
)

# Configure the model generation settings
generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
generation_config.max_new_tokens = 512
generation_config.temperature = 0.1
generation_config.top_p = 0.95
generation_config.do_sample = True
generation_config.repetition_penalty = 1.15

text_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    generation_config=generation_config,
)

llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})

# # Create the prompt template
# template = """
# <s>[INST] <<SYS>> Act as a computer science professor. <</SYS>> {history} {context} {query} [/INST]
# """

# # Create the prompt template
# template = """
# <s>[INST] <sys-instruction> As a computer science professor, respond thoroughly and with academic precision. 
# Provide examples when necessary and relate the response to practical applications in the field. </sys-instruction>
# <sys-context> Historical Context: {history} </sys-context>
# <sys-query> Current Discussion Topic: {context}. Question: {query} </sys-query> [/INST]
# """


# prompt = PromptTemplate(
#     input_variables=["history", "context", "query"],
#     template=template,
# )

# Interaction history queue
history_queue = deque(maxlen=5)  # Stores the last 5 interactions

# def resgen(query, context):
#     # Update the history with the current context and query
#     history_queue.append(f"Context: {context}, Query: {query}")

#     # Create a combined history string
#     history = " ".join(history_queue)

#     # Format the prompt with history, current context, and query
#     formatted_prompt = prompt.format(history=history, context=context, query=query)
#     result = llm(formatted_prompt)
#     return result





#traial stuff - 




# For general discussion
general_discussion_template = PromptTemplate(
    input_variables=["history", "context", "query"],
    template="""
    <s>[INST] <sys-instruction> As a computer science professor, respond with clarity and depth.
    Provide detailed explanations and relevant examples. 
    Dont use greetings in the response, like hi there or hello, and no need to tell who you are, just respond with the dialogue of the professor
    </sys-instruction>
    <sys-context> Historical Context: {history} </sys-context>
    <sys-query> Current Topic: {context}. Inquiry: {query} </sys-query> [/INST]
    """
)

# For specific technical explanations
technical_explanation_template = PromptTemplate(
    input_variables=["history", "context", "query"],
    template="""
    <s>[INST] <sys-instruction> As a computer science professor, focus on technical accuracy and detail.
    Use whatever is necessary and relate the response to underlying theories or algorithms. Dont use greetings in the response, like hi there or hello, and no need to tell who you are, just respond with the dialogue of the professor </sys-instruction>
    <sys-context> Previous interactions: {history} </sys-context>
    <sys-query> Topic of Discussion: {context}. Technical Question: {query} </sys-query> [/INST]
    """
)

# Create Chains for each type of interaction
general_discussion_chain = LLMChain(llm=llm, prompt=general_discussion_template)
technical_explanation_chain = LLMChain(llm=llm, prompt=technical_explanation_template)

# Depending on the nature of the query, decide which chain to use
def resgen(query, context):
    # Update the history with the current context and query
    history_queue.append(f"Context: {context}, Query: {query}")

    if "explain" in query.lower() or "define" in query.lower():
        chain = technical_explanation_chain
    else:
        chain = general_discussion_chain

    # Form the complete history from deque
    history_str = " ".join(history_queue)
    full_text = chain.run({"history": history_str, "context": context, "query": query})

        # Extract the response by finding the marker '[/INST]' and taking the text that follows
    try:
        # Locate the end of the prompt
        response_start_index = full_text.index('[/INST]') + len('[/INST]')
        response = full_text[response_start_index:].strip()
    except ValueError:
        response = "Sorry, I couldn't process your request properly."

    return response



# Example usage
if __name__ == "__main__":
    context = "Today we will discuss neural networks."
    query = "Can you explain what deep learning is?"
    response = resgen(query, context)
    print(response)
    print("next")
    # Example query and context
    query = "What is the role of AI in healthcare?"
    context = """Artificial Intelligence in healthcare is used for diagnoses, treatment recommendations, and patient monitoring. AI can analyze complex medical data much faster than a human doctor and predict diseases early."""
    response = resgen(query, context)
    print(response)
    print ("next! ")
    # Example query and context
    query = "Explain Tokenisation in NLP?"
    context = """Tokenization is the process of replacing sensitive data with a surrogate value, or token, that is non-sensitive and randomized. Tokens are unique identifiers that retain all the important information about the data without compromising its security. For example, a credit card number can be replaced with a token, which is a string of randomized characters. 
    Tokenization can also refer to the process of breaking down a sequence of text into smaller parts, known as tokens. These tokens can be as small as characters or as long as words. For example, tokenizing the sentence “I love ice cream” would result in three tokens: “I,” “love,” and “ice cream”. This process is fundamental in natural language processing and text analysis tasks. """
    response = resgen(query, context)
    print(response)
