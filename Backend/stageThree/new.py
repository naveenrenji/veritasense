from torch import cuda, bfloat16
import transformers
from transformers import StoppingCriteria, StoppingCriteriaList

from huggingface_hub import login
import logging
import torch

auth_token = "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"
login(auth_token)
logging.getLogger().setLevel(logging.ERROR)

torch.cuda.empty_cache()

model_id = 'meta-llama/Llama-2-7b-chat-hf'

print(torch.cuda.memory_summary(device=None, abbreviated=False))

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
    token=hf_auth
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

print(torch.cuda.memory_summary(device=None, abbreviated=False))

print(f"Model loaded on {device}")

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id,
    token=hf_auth
)


stop_list = ['\nHuman:', '\n```\n', '\nSpeaker:']

stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]

# define custom stopping criteria object
class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False

stopping_criteria = StoppingCriteriaList([StopOnTokens()])

generate_text = transformers.pipeline(
    model=model, 
    tokenizer=tokenizer,
    return_full_text=True,  # langchain expects the full text
    task='text-generation',
    # we pass model parameters here too
    stopping_criteria=stopping_criteria,  # without this model rambles during chat
    temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
    max_new_tokens=512,  # max number of tokens to generate in the output
    repetition_penalty=1.1  # without this output begins repeating
)


def response_generator(question, context):
    res = generate_text(f"Answer this Question based on the context, you are playing the role of a computer science professor chatbot: {question}\nThis is the context to use - Context: {context}. now respond based on the context -")
    generated_text = res[0]["generated_text"]
     # Find the index of "now respond-" and slice the text from that point forward
    respond_index = generated_text.find("now respond based on the context -")
    if respond_index != -1:
        # Add the length of "now respond-" to start after this substring
        start_index = respond_index + len("now respond based on the context -")
        torch.cuda.memory_summary(device=None, abbreviated=False)
        return generated_text[start_index:].strip()  # Strip to remove any leading/trailing whitespace
    else:
        # If "now respond-" is not found, return the entire generated text
        return generated_text

question = "Explain Tokenisation in NLP?"
context = """Tokenization is the process of replacing sensitive data with a surrogate value, or token, that is non-sensitive and randomized. Tokens are unique identifiers that retain all the important information about the data without compromising its security. For example, a credit card number can be replaced with a token, which is a string of randomized characters. 

Imperva, Inc.
Data & Payment Tokenization Explained - Imperva, Inc.
What is Tokenization. Tokenization replaces a sensitive data element, for example, a bank account number, with a non-sensitive substitute, known as a token. The token is a randomized data string that has no essential or exploitable value or meaning. It is a unique identifier which retains all the pertinent information about the data without compromising its security. A tokenization system links the original data to a token but does not provide any way to decipher the token and reveal the original data. This is in contrast to encryption systems, which allow data to be deciphered using a secret key.

gartner.com
Definition of Tokenization - Gartner Information Technology Glossary
Tokenization refers to a process by which a piece of sensitive data, such as a credit card number, is replaced by a surrogate value known as a token. The sensitive data still generally needs to be stored securely at one centralized location for subsequent reference and requires strong protections around it.
Tokenization can be used to protect sensitive data or to efficiently process large amounts of data. For example, tokenization can prevent criminals from duplicating bank information onto another card. While tokenization cannot safeguard an organization from a data breach, it may mitigate the financial repercussions. 
Tokenization can also refer to the process of breaking down a sequence of text into smaller parts, known as tokens. These tokens can be as small as characters or as long as words. For example, tokenizing the sentence “I love ice cream” would result in three tokens: “I,” “love,” and “ice cream”. This process is fundamental in natural language processing and text analysis tasks. """
response = response_generator(question, context)
print(response)
torch.cuda.memory_summary(device=None, abbreviated=False)
