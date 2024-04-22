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
generation_config.max_new_tokens = 1024
generation_config.temperature = 0.0001
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
    Provide detailed explanations and relevant examples. </sys-instruction>
    <sys-context> Historical Context: {history} </sys-context>
    <sys-query> Current Topic: {context}. Inquiry: {query} </sys-query> [/INST]
    """
)

# For specific technical explanations
technical_explanation_template = PromptTemplate(
    input_variables=["history", "context", "query"],
    template="""
    <s>[INST] <sys-instruction> As a computer science professor, focus on technical accuracy and detail.
    Use diagrams if necessary and relate the response to underlying theories or algorithms. </sys-instruction>
    <sys-context> Previous interactions: {history} </sys-context>
    <sys-query> Topic of Discussion: {context}. Technical Question: {query} </sys-query> [/INST]
    """
)

# Create Chains for each type of interaction
general_discussion_chain = LLMChain(llm=llm, prompt=general_discussion_template)
technical_explanation_chain = LLMChain(llm=llm, prompt=technical_explanation_template)

# Depending on the nature of the query, decide which chain to use
def resgen(query, context, history):
    if "explain" in query.lower() or "define" in query.lower():
        chain = technical_explanation_chain
    else:
        chain = general_discussion_chain

    # Form the complete history from deque
    history_str = " ".join(history)
    response = chain.run({"history": history_str, "context": context, "query": query})
    return response



# Example usage
if __name__ == "__main__":
    context = "Today we will discuss neural networks."
    query = "Can you explain what deep learning is?"
    response = resgen(query, context)
    print(response)
