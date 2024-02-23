from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig
from torch import cuda, bfloat16
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,                         # load the model in 4-bit precision.
    bnb_8bit_quant_type='nf4',                 # type of quantization to use for 4-bit weights.
    bnb_8bit_use_double_quant=True,            # use double quantization for 4-bit weights.
    bnb_8bit_compute_dtype=bfloat16            # compute dtype to use for 4-bit weights.
)
# Make sure to save the model and tokenizer using .save_pretrained()

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
    # Additional model loading code...
    base_model.save_pretrained('./models/Llama-2-13b-chat-hf')
    model.save_pretrained('./models/kings-crown/EM624_QA_Multi')
    tokenizer.save_pretrained('./models/Llama-2-13b-chat-hf-tokenizer')

load_model()