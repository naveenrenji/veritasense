from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import gc  # Garbage Collector
from huggingface_hub import login
from torch.cuda.amp import autocast

access_token = "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"
login(access_token)
model_id = 'kings-crown/EM624_QA_Full'
base_model_id = "meta-llama/Llama-2-13b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(base_model_id, token=access_token)
model = AutoModelForCausalLM.from_pretrained(model_id, token=access_token)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
if torch.cuda.device_count() > 1:
    model = torch.nn.DataParallel(model)

text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device.type == 'cuda' else -1)

def check_and_clear_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def response_generator(question, context):
    check_and_clear_memory()  
    with torch.no_grad(): 
        prompt = f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -"
        with autocast(): 
            generated_responses = text_gen_pipeline(prompt, truncation=True, max_length=512, num_return_sequences=1, temperature=0.7)
    generated_text = generated_responses[0]['generated_text']
    respond_index = generated_text.find("now respond based on the context -") + len("now respond based on the context -")
    response = generated_text[respond_index:].strip()
    check_and_clear_memory()  
    return response

# Example usage
question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context)
print(response)
