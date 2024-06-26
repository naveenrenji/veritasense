from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import gc  
from huggingface_hub import login

access_token = "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"
login(access_token)


model_id = 'kings-crown/EM624_QA_Full'
base_model_id = "meta-llama/Llama-2-13b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_auth_token=access_token)
model = AutoModelForCausalLM.from_pretrained(model_id, use_auth_token=access_token)

print(torch.cuda.memory_summary(device=None, abbreviated=False))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
if torch.cuda.device_count() > 1:
    print(f"Gpu counts just for me to see : {torch.cuda.device_count()} ")
    model = torch.nn.DataParallel(model)

print(torch.cuda.memory_summary(device=None, abbreviated=False))

text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device.type == 'cuda' else -1)

def check_and_clear_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def response_generator(question, context):
    check_and_clear_memory()

    with torch.no_grad():  
        prompt = f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -"
        generated_responses = text_gen_pipeline(prompt, truncation=True, max_length=512, num_return_sequences=1, temperature=0.7)

    generated_text = generated_responses[0]['generated_text']
    respond_index = generated_text.find("now respond based on the context -") + len("now respond based on the context -")
    response = generated_text[respond_index:].strip()
    check_and_clear_memory() 
    return response

question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context)
torch.cuda.synchronize()
print(response)

question = "Explain Tokenisation in NLP?"
context = """Tokenization is the process of replacing sensitive data with a surrogate value, or token, that is non-sensitive and randomized. Tokens are unique identifiers that retain all the important information about the data without compromising its security. For example, a credit card number can be replaced with a token, which is a string of randomized characters. 
Tokenization can also refer to the process of breaking down a sequence of text into smaller parts, known as tokens. These tokens can be as small as characters or as long as words. For example, tokenizing the sentence “I love ice cream” would result in three tokens: “I,” “love,” and “ice cream”. This process is fundamental in natural language processing and text analysis tasks. """
response = response_generator(question, context)
torch.cuda.synchronize()
print(response)
