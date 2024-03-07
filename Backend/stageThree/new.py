from torch import cuda, bfloat16
import transformers
from transformers import StoppingCriteria, StoppingCriteriaList, pipeline

from huggingface_hub import login
import logging
import torch

auth_token = "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"
login(auth_token)
logging.getLogger().setLevel(logging.ERROR)


model_id = 'meta-llama/Llama-2-7b-chat-hf'

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

# set quantization configuration to load large model with less GPU memory
# this requires the `bitsandbytes` library
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

# begin initializing HF items, you need an access token
hf_auth = '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'
model_config = transformers.AutoConfig.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)


model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    quantization_config=bnb_config,
    device_map='auto',
    token=hf_auth
)

# enable evaluation mode to allow model inference
model.eval()

print(f"Model loaded on {device}")

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id,
    token=hf_auth
)


# Define custom stopping criteria
class StopOnTokens(StoppingCriteria):
    def __init__(self, stop_token_ids):
        self.stop_token_ids = stop_token_ids

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in self.stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False

# Generate text function
def generate_text(question, context):
    stop_list = ['\nHuman:', '\n```\n', '\nSpeaker:']
    stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
    stop_token_ids = [torch.tensor(x, dtype=torch.long) for x in stop_token_ids]

    stopping_criteria = StoppingCriteriaList([StopOnTokens(stop_token_ids)])

    text_generator = pipeline(
        model=model,
        tokenizer=tokenizer,
        task='text-generation',
        stopping_criteria=stopping_criteria,
        temperature=0.1,
        max_new_tokens=512,
        repetition_penalty=1.1
    )

    res = text_generator(f"Question: {question}\nContext: {context}. now respond-")
    return res[0]["generated_text"]

result = generate_text("Explain the difference between Data Lakehouse and Data Warehouse.", "Cloud Data")
print(result)
