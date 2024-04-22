import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

# Setup model directory
model_dir = './models/Llama-2-13b-Chat-GPTQ'
MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"

# Ensure the directory exists
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Initialize and save model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
tokenizer.save_pretrained(model_dir)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto")
model.save_pretrained(model_dir)

# Create and save configuration
generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
generation_config.max_new_tokens = 512
generation_config.temperature = 0.1
generation_config.top_p = 0.95
generation_config.do_sample = True
generation_config.repetition_penalty = 1.15
generation_config.save_pretrained(model_dir)

print("Model and tokenizer have been saved to:", model_dir)
