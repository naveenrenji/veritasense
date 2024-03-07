from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
from torch import cuda
from huggingface_hub import login
import torch
import os

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

def load_model():
    model_id = 'kings-crown/EM624_QA_Full'
    base_model_id = "meta-llama/Llama-2-7b-chat-hf"
    access_token = "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"
    login(access_token)
    
    try:
        # Assuming PeftModel.from_pretrained can directly accept model_id
        model = PeftModel.from_pretrained(base_model_id, model_id, token=access_token, device_map="auto")
        tokenizer = AutoTokenizer.from_pretrained(base_model_id, token=access_token)
    except Exception as e:
        print(f"An error occurred while loading the model or tokenizer: {e}")
        raise

    return model, tokenizer

def response_generator(question, context, model, tokenizer, max_length=512, temperature=0.1):
    conversation_history = []  # Local management of conversation history

    # Format the conversation history with the new question and context
    conversation_history.append(f"User: {question}\nContext: {context}")

    # Ensure conversation history does not exceed 10 exchanges
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    formatted_input = "\n".join(conversation_history)

    # Tokenize input and generate response
    inputs = tokenizer(formatted_input, return_tensors="pt", padding=True, truncation=True).to(model.device)
    outputs = model.generate(**inputs, max_length=max_length, temperature=temperature, num_return_sequences=1)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Append the response to the conversation history
    conversation_history.append(f"Assistant: {response_text}")

    return response_text

# Load the model and tokenizer once
model, tokenizer = load_model()

# Example usage
question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context, model, tokenizer)
print(response)
