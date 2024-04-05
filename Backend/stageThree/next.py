from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from huggingface_hub import login
import gc  # Garbage Collector

print ("Allocated is = ", torch.cuda.memory_reserved())
def check_and_clear_memory(threshold_gb=30):
    threshold_bytes = threshold_gb * 1024 ** 3
    total_memory = torch.cuda.get_device_properties(0).total_memory
    reserved_memory = torch.cuda.memory_reserved(0)
    allocated_memory = torch.cuda.memory_allocated(0)

    if (reserved_memory + allocated_memory) > threshold_bytes:
        print("Clearing Memory...")
        torch.cuda.empty_cache()
        gc.collect()
        print("Memory Cleared.")
check_and_clear_memory()

def load_model():
    model_id = 'kings-crown/EM624_QA_Full'
    base_model_id = "meta-llama/Llama-2-13b-chat-hf"
    access_token = "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"
    
    login(access_token)
    
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_auth_token=access_token)
    model = AutoModelForCausalLM.from_pretrained(model_id, token=access_token)
    
    if torch.cuda.device_count() > 1:  # Check if more than one GPU is available
        print(f"Let's use {torch.cuda.device_count()} GPUs!")
        model = torch.nn.DataParallel(model)  # Wrap the model for DataParallel
    
    model.to('cuda')  # Move the model to the default CUDA device

    return model, tokenizer


model, tokenizer = load_model()

def response_generator(question, context):
    check_and_clear_memory()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)  # Ensure the model is on the right device

    text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device.type == 'cuda' else -1)
    
    prompt = f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -"
    generated_responses = text_gen_pipeline(prompt, truncation=True, max_length=512, num_return_sequences=1, temperature=0.7)

    generated_text = generated_responses[0]['generated_text']
    respond_index = generated_text.find("now respond based on the context -") + len("now respond based on the context -")
    response = generated_text[respond_index:].strip()

    return response

# Example usage
question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context)
print(response)
