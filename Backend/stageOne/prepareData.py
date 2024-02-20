# prepare_data.py

import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer
import os
import pickle
import numpy as np

# Functions to save and load objects using pickle
def save_obj(obj, name):
    with open(os.path.join(BASE_DIR, name + '.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# Set the base directory to the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize and prepare data
def init_data():
    csv_file = os.path.join(BASE_DIR, "questions_answers.csv")
    df = pd.read_csv(csv_file)

    model_path = './models/all-MiniLM-L6-v2'  
    model = SentenceTransformer(model_path)
    
    spacy.cli.download("en_core_web_sm")
    spacy_tokenizer = spacy.load('en_core_web_sm')
    questions = [spacy_tokenizer(question).text for question in df['question']]
    save_obj(questions, 'questions')

    question_embeddings = np.array(model.encode(questions, show_progress_bar=True))
    save_obj(question_embeddings, 'question_embeddings')

# Main function to run the script for data preparation
if __name__ == '__main__':
    init_data()
