from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModelForCausalLM, PeftConfig
from torch import cuda, bfloat16
import transformers
bnb_config = transformers.BitsAndBytesConfig(
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
    model = transformers.AutoModelForCausalLM.from_pretrained(
        config.base_model_name_or_path,
        return_dict=True,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    return model, tokenizer
def generate_response(model, tokenizer, query):
    inputs = tokenizer.encode(query, return_tensors='pt')
    output = model.generate(inputs, max_length=512, num_return_sequences=1, temperature=1.0)
    response_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return response_text
def main():
    model, tokenizer = load_model()
    print("Model loaded. You can start chatting. Type 'quit' to exit.")
    while True:
        query = input("You: ")
        if query.lower() == 'quit':
            break
        response = generate_response(model, tokenizer, query)
        print("Bot:", response)
if __name__ == "__main__":
    main()





