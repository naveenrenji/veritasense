from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import logging

auth_token = "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"
login(auth_token)
logging.getLogger().setLevel(logging.ERROR)

# Load the PEFT-configured LLaMa model
config = PeftConfig.from_pretrained("kings-crown/EM624_QA_Full")
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
model = PeftModel.from_pretrained(base_model, "kings-crown/EM624_QA_Full")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")

def response_generator(question, context):
    conversation_history = []

    # Append the new user's question to the conversation history
    conversation_history.append({
        "role": "user",
        "content": f"Question: {question}\nContext: {context}. now respond-"
    })

    # Truncate the conversation history to the last 5 exchanges
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    # Format the conversation history for the model
    formatted_input = "\n".join([f"{exchange['role']}: {exchange['content']}" for exchange in conversation_history])

    # Generate a response using the LLaMa model
    inputs = tokenizer.encode(formatted_input, return_tensors="pt")
    output = model.generate(inputs, max_length=60, num_return_sequences=1, temperature=0.1)
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


question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context)
print(response)
