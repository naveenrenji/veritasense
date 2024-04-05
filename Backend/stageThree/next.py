from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch
from huggingface_hub import login

def load_model():
    model_id = 'kings-crown/EM624_QA_Full'
    base_model_id = "meta-llama/Llama-2-13b-chat-hf"
    access_token = "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"
    
    # Log in to Hugging Face
    login(access_token)
    
    # Set up BitsAndBytes configuration for 8-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_8bit=True,
        bnb_8bit_quant_type='nf4',
        bnb_8bit_use_double_quant=True,
        bnb_8bit_compute_dtype=torch.bfloat16
    )
    
    # Load the tokenizer and the model with BitsAndBytes configuration
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_auth_token=access_token)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        use_auth_token=access_token,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        revision="main",
        low_cpu_mem_usage=True
    )
    
    return model, tokenizer

model, tokenizer = load_model()

def response_generator(question, context):
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
