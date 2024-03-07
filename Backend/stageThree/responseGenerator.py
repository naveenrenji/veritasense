from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from torch import bfloat16
from huggingface_hub import login
import transformers
auth_token = "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"
# Configure the BitsAndBytes quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,                         # Load the model in 4-bit precision
    bnb_4bit_quant_type='nf4',                 # Type of quantization for 4-bit weights
    bnb_4bit_use_double_quant=True,            # Use double quantization for 4-bit weights
    bnb_4bit_compute_dtype=bfloat16            # Compute dtype for 4-bit weights
)
login(auth_token)
# Load the PEFT-configured LLaMa model
config = PeftConfig.from_pretrained("kings-crown/EM624_QA_Full", token=auth_token)
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", token=auth_token)
model = PeftModel.from_pretrained(base_model, "kings-crown/EM624_QA_Full", token=auth_token,device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
generator = transformers.pipeline(
    model=model, tokenizer=tokenizer,
    task='text-generation',
    temperature=0.1,
    max_new_tokens=500,
    repetition_penalty=1.1
)
prompt = "Could you explain to me how 4-bit quantization works as if I am 5?"
res = generator(prompt)
print(res[0]["generated_text"])




