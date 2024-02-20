import csv
import re

def clean_data(text):
    """ Removes specific characters and splits the text into lines. """
    text = re.sub(r"---|\*", "", text) 
    return text.split('\n')

def process_entry(lines):
    """ Processes lines to extract and return the four components. """
    components = {'Question': '', 'Response': '', 'Context': '', 'Category': ''}
    for line in lines:
        for key in components:
            if line.startswith(f"{key}:"):
                components[key] = line.replace(f"{key}:", "").strip()

    if all(components.values()):
        return [components['Question'], components['Response'], components['Context'], components['Category']]
    else:
        return None

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['Question', 'Response', 'Context', 'Category'])

        text = " ".join([" ".join(row) for row in reader])
        lines = clean_data(text)

        entry = []
        for line in lines:
            if line.startswith(("Question:", "Response:", "Context:", "Category:")):
                if entry:
                    processed_entry = process_entry(entry)
                    if processed_entry:
                        writer.writerow(processed_entry)
                    entry = []
                entry.append(line)

        # Process the last entry if exists
        if entry:
            processed_entry = process_entry(entry)
            if processed_entry:
                writer.writerow(processed_entry)

input_file_path = 'output.csv'
output_file_path = 'cleaned_output.csv'

process_csv(input_file_path, output_file_path)
