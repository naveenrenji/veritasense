from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from huggingface_hub import login
import gc  # Garbage Collector

# Function to clear cache if GPU memory usage exceeds the threshold
def check_and_clear_memory(threshold_gb=30):
    # Convert GB to bytes
    threshold_bytes = threshold_gb * 1024 ** 3

    # Get the current GPU memory usage
    total_memory = torch.cuda.get_device_properties(0).total_memory
    reserved_memory = torch.cuda.memory_reserved(0)
    allocated_memory = torch.cuda.memory_allocated(0)
    free_memory = total_memory - (reserved_memory + allocated_memory)

    print(f"Total GPU Memory: {total_memory / (1024 ** 3):.2f} GB, Used GPU Memory: {(reserved_memory + allocated_memory) / (1024 ** 3):.2f} GB, Free GPU Memory: {free_memory / (1024 ** 3):.2f} GB")

    # Check if used memory exceeds the threshold
    if (reserved_memory + allocated_memory) > threshold_bytes:
        print("Clearing Memory...")
        # Clear PyTorch's cache
        torch.cuda.empty_cache()
        # Explicitly collect garbage
        gc.collect()
        print("Memory Cleared.")

# Your existing function to load the model
def load_model():
    model_id = 'kings-crown/EM624_QA_Full'
    base_model_id = "meta-llama/Llama-2-13b-chat-hf"
    access_token = "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"
    
    # Log in to Hugging Face
    login(access_token)
    
    # Load the tokenizer and the model
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_auth_token=access_token)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=access_token,
        device_map="auto",
        revision="main",
    )
    
    return model, tokenizer

# Initialize your model and tokenizer
model, tokenizer = load_model()

def response_generator(question, context):
    # Check and clear memory if necessary before generating the response
    check_and_clear_memory()

    # Ensure model and tokenizer are moved to the appropriate device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Initialize the pipeline for text-generation with the model and tokenizer
    text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device.type == 'cuda' else -1)
    
    # Generate the response based on the context and question
    prompt = f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -"
    generated_responses = text_gen_pipeline(prompt, max_length=512, num_return_sequences=1, temperature=0.7)
    
    # Extract and clean up the response
    generated_text = generated_responses[0]['generated_text']
    respond_index = generated_text.find("now respond based on the context -") + len("now respond based on the context -")
    response = generated_text[respond_index:].strip()  # Strip to remove any leading/trailing whitespace

    return response

# Example usage
question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context)
print(response)
