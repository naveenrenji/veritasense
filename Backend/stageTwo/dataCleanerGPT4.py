import openai
import csv

def read_text_file(file_path, chunk_size):
    with open(file_path, 'r') as file:
        text = file.read()
        sentences = text.split('.')
        chunks = []
        i = 0
        while i < len(sentences):
            chunk = ''
            for j in range(i, min(i + chunk_size, len(sentences))):
                chunk += sentences[j].strip() + '. '
            if i + chunk_size < len(sentences):
                overlap = int(chunk_size * 0.15)
                i += (chunk_size - overlap)
            else:
                i += chunk_size
            chunks.append(chunk)
        return chunks

def process_chunks(chunks, api_key):
    openai.api_key = api_key
    results = []

    for chunk in chunks:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                          {"role": "user", "content": f"Cut up each chunk of text into many small paragraphs and re-write them as Question, response, context and category sets. Do your best to format the question-answer pairs to include as many technical explanations as possible. Keep the format of the pairs consistent throughout, do not add question numbers and fit as many pairs as possible in one response. If any names are mentioned, replace them with 'speaker'.\n\n{chunk}"}]
            )
            print(response.choices[0].message['content'].strip())
            results.append(response.choices[0].message['content'].strip())
        except Exception as e:
            print(f"Error processing chunk: {e}")

    return results

def save_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Response', 'Context', 'Category'])

        for entry in data:
            rows = entry.split('\n')
            for row in rows:
                if row.strip():
                    writer.writerow(row.split('|'))

def main():
    file_path = 'sseData.txt' 
    api_key = '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'  
    chunk_size = 50 

    chunks = read_text_file(file_path, chunk_size)
    processed_data = process_chunks(chunks, api_key)
    save_to_csv(processed_data, 'output.csv')

if __name__ == '__main__':
    main()
