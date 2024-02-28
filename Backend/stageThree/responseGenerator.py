# Conduct query with retrieval of sources
query = "tell me about myself"
source_information ="My name is Naveen I am a boy forom bahrain and i love to play agmes with all my fiendds"
combined_information = f"Query: {query}\nContinue to answer the query by using the context: \n{source_information}."
print(combined_information)
auth_token = "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"
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=auth_token)
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=auth_token)
# tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")

# # CPU Enabled uncomment below 👇🏽
# model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it")
# GPU Enabled use below 👇🏽
# model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it", use_auth_token=auth_token, device_map="auto")

# Moving tensors to GPU
input_ids = tokenizer(combined_information, return_tensors="pt").to("cuda")
response = model.generate(**input_ids, max_new_tokens=500)
print(tokenizer.decode(response[0]))