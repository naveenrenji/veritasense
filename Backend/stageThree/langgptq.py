import torch
from langchain import HuggingFacePipeline, PromptTemplate, LLMChain
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

# Create the prompt template
template = """
<s>[INST] <sys-instruction> As a computer science professor, respond thoroughly and with academic precision. 
Provide examples when necessary and relate the response to practical applications in the field. </sys-instruction>
<sys-context> Historical Context: {history} </sys-context>
<sys-query> Current Discussion Topic: {context}. Question: {query} </sys-query> [/INST]
"""


prompt = PromptTemplate(
    input_variables=["history", "context", "query"],
    template=template,
)

# Interaction history queue
history_queue = deque(maxlen=5)  # Stores the last 5 interactions

def resgen(query, context):
    # Update the history with the current context and query
    history_queue.append(f"Context: {context}, Query: {query}")

    # Create a combined history string
    history = " ".join(history_queue)

    # Format the prompt with history, current context, and query
    formatted_prompt = prompt.format(history=history, context=context, query=query)
    result = llm(formatted_prompt)
    return result

# Example usage
if __name__ == "__main__":
    context = "Today we will discuss neural networks."
    query = "Can you explain what deep learning is?"
    response = resgen(query, context)
    print(response)
