from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Initialize the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Set the model to evaluation mode
model.eval()

# Check if CUDA is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_response(question, context):
    # Encode the context and question to tensor format
    input_text = context + "\nQuestion: " + question + "\nAnswer:"
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)

    # Generate response using the model
    outputs = model.generate(
        input_ids,
        max_length=512,  # Maximum length for the output text
        num_return_sequences=1,  # Number of responses to generate
        no_repeat_ngram_size=2,  # Ensures the model does not repeat n-grams
        temperature=0.7,  # Controls randomness: lower is less random
        top_p=0.9,  # Nucleus sampling: top p% probability mass
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode the output tokens to string
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
        # Extract the answer part after "Answer:"
    answer_start = response.find("Answer:") + len("Answer:")
    answer = response[answer_start:].strip()

    # Print only the answer
    print(answer)

# Example question and context
question = "What is the role of AI in healthcare?"
context = """Artificial Intelligence in healthcare is used for diagnoses, treatment recommendations, and patient monitoring. AI can analyze complex medical data much faster than a human doctor and predict diseases early."""

# Generate and print the response
generate_response(question, context)
