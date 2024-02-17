from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig
from torch import cuda, bfloat16


bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,                         # load the model in 4-bit precision.
    bnb_4bit_quant_type='nf4',                 # type of quantization to use for 4-bit weights.
    bnb_4bit_use_double_quant=True,            # use double quantization for 4-bit weights.
    bnb_4bit_compute_dtype=bfloat16            # compute dtype to use for 4-bit weights.
)

def load_model():
    model_id = 'kings-crown/EM624_QA_Multi'
    base_model_id = "meta-llama/Llama-2-13b-chat-hf"
    access_token = "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"
    base_model = AutoModelForCausalLM.from_pretrained(base_model_id, use_auth_token=access_token)
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_auth_token=access_token)
    config = PeftConfig.from_pretrained(model_id, use_auth_token=access_token)
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model_name_or_path,
        return_dict=True,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    return model, tokenizer


conversation_history = []

def response_generator(model, tokenizer, question, context):
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

    # Generate a response using the model
    inputs = tokenizer.encode(formatted_input, return_tensors="pt")
    inputs = inputs.to(model.device)
    output = model.generate(inputs, max_length=512, num_return_sequences=1, temperature=0.1)
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
    model, tokenizer = load_model()
    print("Model loaded. You can start chatting. Type 'quit' to exit.")
    
    while True:
        question = input("You: ")
        if question.lower() == 'quit':
            break
        response = response_generator(model, tokenizer, question, "")
        print("Bot:", response)

if __name__ == "__main__":
    main()
