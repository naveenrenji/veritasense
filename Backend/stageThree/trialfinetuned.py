from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel, PeftConfig
from torch import bfloat16
import torch
from huggingface_hub import login
import transformers

# Function to set up and configure the model and tokenizer
def setup_model(auth_token, model_id="kings-crown/EM624_QA_Full", base_model_id="meta-llama/Llama-2-7b-chat-hf"):
    # Log in to Hugging Face
    login(auth_token)

    print("CUDA Available:", torch.cuda.is_available())
    print("Current Device:", torch.cuda.current_device() if torch.cuda.is_available() else "CPU")

    # Load the PEFT-configured model
    config = PeftConfig.from_pretrained(model_id, token=auth_token)
    base_model = AutoModelForCausalLM.from_pretrained(base_model_id, token=auth_token)
    model = PeftModel.from_pretrained(base_model, model_id, token=auth_token, device_map="auto")
    
    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    
    # Create the generation pipeline
    generator = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        temperature=0.1,
        max_new_tokens=500,
        repetition_penalty=1.1
    )
    
    return generator

# Response generator function
def response_generator(question, context, auth_token="your_auth_token_here"):
    # Replace 'your_auth_token_here' with your actual Hugging Face auth token
    generator = setup_model(auth_token)
    
    # Format the prompt with the question and context
    prompt = f"Respond to this Question based on the provided context mainly, respond with just your answer: {question} \nContext to use : {context}"
    
    # Generate the response
    res = generator(prompt)
    
    # Extract and return the generated text
    return res[0]["generated_text"]

# Example usage:
question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context, auth_token="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")
print(response)
