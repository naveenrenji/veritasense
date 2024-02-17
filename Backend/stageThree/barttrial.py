from transformers import BartTokenizer, BartForConditionalGeneration
from time import time

# Load the fine-tuned BART model and tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')

def generate_response(text_information, user_query):

    t = time()
    # Combine text information and user query to form the input
    input_text = f"The information I have is: '{text_information}'. Now, to your question: '{user_query}'"

    # Tokenize the input text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate the response using the model
    response = model.generate(inputs, max_length=512, num_return_sequences=1, temperature=1.0)

    # Decode and return the response text
    response_text = tokenizer.decode(response[0], skip_special_tokens=True)
    
    print('Time to generate the response:', round(time() - t, 4), 'seconds')

    return response_text

# # Example:

# # Generate the response using the BART model
# response = generate_response(text_information, user_query)

# Print the response
#print(response)
