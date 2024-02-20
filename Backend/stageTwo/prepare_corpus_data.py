# prepare_corpus_data.py

import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer
import os
import pickle

# Set the base directory to the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to save object
def save_obj(obj, name):
    with open(os.path.join(BASE_DIR, name + '.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# Initialize and prepare data
def prepare_corpus():
    # Correct the model path to be absolute or ensure it's correctly relative to where the script runs
    model_path = './models/all-roberta-large-v1'
    model = SentenceTransformer(model_path)

    # Make sure the SpaCy model is available
    # If you're unsure, you can add spacy.cli.download('en_core_web_sm') here
    spacy_tokenizer = spacy.load('en_core_web_sm')
    corpus_file = os.path.join(BASE_DIR, 'sseData.txt')

    if os.path.exists(os.path.join(BASE_DIR, 'corpus_sentences.pkl')) and os.path.exists(os.path.join(BASE_DIR, 'corpus_embeddings.pkl')):
        print("Corpus data already prepared.")
    else:
        with open(corpus_file, 'r') as f:
            corpus = f.read()

        # Tokenization might not need splitting text into words, so adjust based on your needs
        corpus_sentences = [sentence.strip() for sentence in corpus.split('.') if sentence]

        corpus_embeddings = model.encode(corpus_sentences, show_progress_bar=True)
        
        # Save tokenized sentences and embeddings
        save_obj(corpus_sentences, 'corpus_sentences')
        save_obj(corpus_embeddings, 'corpus_embeddings')

        print("Corpus data prepared and saved.")

# Main function to run the script for corpus data preparation
if __name__ == '__main__':
    prepare_corpus()
