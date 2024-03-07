import torch
from transformers import pipeline, StoppingCriteria, StoppingCriteriaList, AutoTokenizer, AutoModelForCausalLM

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained('./models/Llama-2-7b-chat-hf')
tokenizer = AutoTokenizer.from_pretrained('./models/Llama-2-7b-chat-hf-tokenizer')

# Ensure the model is in evaluation mode
model.eval()

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

result = generate_text("Explain the difference between Data Lakehouse and Data Warehouse.")
print(result)
