from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import warnings

# Suppress warnings from the transformers library
warnings.filterwarnings("ignore", category=UserWarning)

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
print ("next! ")

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
generate_response(question, context)
