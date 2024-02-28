from transformers import AutoTokenizer, AutoModelForCausalLM

def response_generator(question, context):
    auth_token = "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"
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=auth_token)
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=auth_token, device_map="auto")
    # tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
    combined_information = f"Query: {question}\nContinue to answer the query by using the context: \n{context}."

    # # CPU Enabled uncomment below 👇🏽
    # model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it")
    # GPU Enabled use below 👇🏽
    # model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it", use_auth_token=auth_token, device_map="auto")

    # Moving tensors to GPU
    input_ids = tokenizer(combined_information, return_tensors="pt").to("cuda")
    response = model.generate(**input_ids, max_new_tokens=500)
    return (tokenizer.decode(response[0]))