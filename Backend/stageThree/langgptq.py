import torch
from langchain import HuggingFacePipeline, PromptTemplate, LLMChain
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
from huggingface_hub import login
access_token = "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"
login(access_token)

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

# Create the prompt template
template = """
<s>[INST] <<SYS>> Act as a computer science professor. <</SYS>> {context} {query} [/INST]
"""

prompt = PromptTemplate(
    input_variables=["context", "query"],
    template=template,
)

# Define the function resgen to generate responses based on the query and context
def resgen(query, context):
    formatted_prompt = prompt.format(context=context, query=query)
    result = llm(formatted_prompt)
    return result

# Example usage
if __name__ == "__main__":
    context = "Today we will discuss neural networks."
    query = "Can you explain what deep learning is?"
    response = resgen(query, context)
    print(response)
