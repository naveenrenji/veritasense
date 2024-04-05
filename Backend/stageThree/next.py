from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import logging
import torch
import transformers
from transformers import StoppingCriteria, StoppingCriteriaList
from torch import cuda, bfloat16


auth_token = "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"
login(auth_token)
logging.getLogger().setLevel(logging.ERROR)

# Load the PEFT-configured LLaMa model
config = PeftConfig.from_pretrained("kings-crown/EM624_QA_Full")
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
model = PeftModel.from_pretrained(base_model, "kings-crown/EM624_QA_Full")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")


# Set device and quantization configuration
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)
model = model.to(device, bnb_config.to_tensor_dict_func)

# Enable evaluation mode
model.eval()
print(f"Model loaded on {device}")

stop_list = ['\\nHuman:', '\\n```\\n', '\\nSpeaker:']
stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]

# Define custom stopping criteria object
class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False

stopping_criteria = StoppingCriteriaList([StopOnTokens()])

def response_generator(question, context):
    res = model.generate(
        **tokenizer.prepare_seq2seq_batch(
            f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -",
            max_length=512,
            num_return_sequences=1,
            temperature=0.1,
            stopping_criteria=stopping_criteria
        )
    )
    generated_text = tokenizer.decode(res[0], skip_special_tokens=True)

    # Find the index of "now respond-" and slice the text from that point forward
    respond_index = generated_text.find("now respond based on the context -")
    if respond_index != -1:
        start_index = respond_index + len("now respond based on the context -")
        return generated_text[start_index:].strip()
    else:
        return generated_text

question = "What is AI?"
context = "Artificial Intelligence is a field of computer science."
response = response_generator(question, context)
print(response)