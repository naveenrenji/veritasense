from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import gc  # Garbage Collector
from huggingface_hub import login

# Login once at the start
access_token = "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"
login(access_token)

# Load model and tokenizer once
model_id = 'kings-crown/EM624_QA_Full'
base_model_id = "meta-llama/Llama-2-13b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_auth_token=access_token)
model = AutoModelForCausalLM.from_pretrained(model_id, use_auth_token=access_token)

# Move model to GPU if available and use DataParallel if multiple GPUs are available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
if torch.cuda.device_count() > 1:
    print(f"Let's use {torch.cuda.device_count()} GPUs!")
    model = torch.nn.DataParallel(model)

# Initialize the pipeline once
text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device.type == 'cuda' else -1)

def check_and_clear_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def response_generator(question, context):
    check_and_clear_memory()

    with torch.no_grad():  # No gradient computation for inference
        prompt = f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -"
        generated_responses = text_gen_pipeline(prompt, truncation=True, max_length=512, num_return_sequences=1, temperature=0.7)

    generated_text = generated_responses[0]['generated_text']
    respond_index = generated_text.find("now respond based on the context -") + len("now respond based on the context -")
    response = generated_text[respond_index:].strip()

    check_and_clear_memory()  # Clear memory after generating each response
    return response

# Example usage
question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context)
print(response)
