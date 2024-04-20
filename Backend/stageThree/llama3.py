from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "meta-llama/Meta-Llama-3-8B"
prompt = "Tell me about gravity"
access_token = "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"



model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", load_in_4bit=True,  use_auth_token=access_token)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, use_auth_token=access_token)
model_inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")

output = model.generate(**model_inputs)

print(tokenizer.decode(output[0], skip_special_tokens=True))