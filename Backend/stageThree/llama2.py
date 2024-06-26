from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
auth_token = "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"
login(auth_token)


model_name = "meta-llama/Llama-2-7b-chat-hf"
question = "Explain Tokenisation in NLP?"
context = """Tokenization is the process of replacing sensitive data with a surrogate value, or token, that is non-sensitive and randomized. Tokens are unique identifiers that retain all the important information about the data without compromising its security. For example, a credit card number can be replaced with a token, which is a string of randomized characters. 
Tokenization can also refer to the process of breaking down a sequence of text into smaller parts, known as tokens. These tokens can be as small as characters or as long as words. For example, tokenizing the sentence “I love ice cream” would result in three tokens: “I,” “love,” and “ice cream”. This process is fundamental in natural language processing and text analysis tasks. """
prompt = f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -"

model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", load_in_4bit=True,  token=auth_token)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True,return_token_type_ids=False, token=auth_token)
model_inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")

output = model.generate(**model_inputs)

print(tokenizer.decode(output[0], skip_special_tokens=True))
