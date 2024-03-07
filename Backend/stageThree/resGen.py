from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig
from torch import cuda, bfloat16
import os
import torch
from huggingface_hub import login

# # Set environment variable to reduce TensorFlow logging
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# # Define your Hugging Face access token here
auth_token = "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"
login(auth_token)
torch.cuda.empty_cache()
# Configure the BitsAndBytes quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,                         # Load the model in 4-bit precision
    bnb_4bit_quant_type='nf4',                 # Type of quantization for 4-bit weights
    bnb_4bit_use_double_quant=True,            # Use double quantization for 4-bit weights
    bnb_4bit_compute_dtype=bfloat16            # Compute dtype for 4-bit weights
)

# Load the PEFT-configured LLaMa model
config = PeftConfig.from_pretrained("kings-crown/EM624_QA_Full", token=auth_token)
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-chat-hf", token=auth_token, device_map="auto",)
model = PeftModel.from_pretrained(base_model, "kings-crown/EM624_QA_Full", token=auth_token, device_map="auto",)
model = model.to("cuda")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=auth_token)
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=auth_token, device_map="auto")
conversation_history = []

def response_generator(question, context):
    print("started generation")

    global conversation_history

    # Append the new user's question to the conversation history
    conversation_history.append({
        "role": "user",
        "content": f"Question: {question}\nContext: {context}"
    })

    # Truncate the conversation history to the last 5 exchanges
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    # Format the conversation history for the model
    formatted_input = "\n".join([f"{exchange['role']}: {exchange['content']}" for exchange in conversation_history])

    # Generate a response using the LLaMa model
    inputs = tokenizer.encode(formatted_input, return_tensors="pt").to("cuda")
    output = model.generate(inputs, max_length=512, num_return_sequences=1, temperature=1.0)
    response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Append the model's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": response_text
    })

    # Truncate the conversation history if necessary
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    return response_text


def main():
    print("inside main")
    while True:
        userinput = input("User: ")
        if userinput.lower() == "stop":
            break
        else:
            response = response_generator(userinput, "My name is Naveen, I am from Bahrain, I love shopping and playing football. My hobbies include reading and dancing.")
            print(f"Assistant: {response}")

main()