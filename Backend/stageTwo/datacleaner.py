import re

def clean_text(text):
    # Remove special characters except for periods
    cleaned_text = re.sub(r'[^a-zA-Z0-9.\s]', '', text)
    
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    # Remove single characters that don't form a word, but keep periods
    cleaned_text = ' '.join([word if word != '.' else '.' for word in cleaned_text.split() if len(word) > 1 or word == '.'])
    
    # Ensure periods are followed by a space for sentence tokenization
    cleaned_text = cleaned_text.replace('.', '. ')
    
    return cleaned_text

def read_and_clean_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        raw_text = infile.read()
        
    cleaned_text = clean_text(raw_text)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(cleaned_text)

# Read from 'combined.txt' and write cleaned data to 'sseData.txt'
read_and_clean_file('combined.txt', 'sseData.txt')
