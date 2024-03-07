from transformers import AutoModelForCausalLM, AutoConfig, AutoTokenizer
import transformers
import torch
from huggingface_hub import login

# Authentication token and model ID
auth_token = "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"
model_id = 'meta-llama/Llama-2-7b-chat-hf'

# Login to Hugging Face
login(auth_token)

# Model configuration
model_config = AutoConfig.from_pretrained(model_id, use_auth_token=auth_token)

# Set quantization configuration to load large model with less GPU memory
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Download and save the model
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    quantization_config=bnb_config,
    device_map='auto',
    token=auth_token
)
model.save_pretrained('./models/Llama-2-7b-chat-hf')

# Download and save the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id, token=auth_token)
tokenizer.save_pretrained('./models/Llama-2-7b-chat-hf-tokenizer')
