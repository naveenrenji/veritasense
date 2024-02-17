import pinecone as pc
from sentence_transformers import SentenceTransformer
import spacy
import pickle
import os
from time import time

t = time()

# Load the sentence transformer model
model_name = 'sentence-transformers/all-roberta-large-v1'
model = SentenceTransformer(model_name)

# Function to save object
def save_obj(obj, name):
    with open(os.path.join(os.path.dirname(__file__), name + '.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# Function to load object
def load_obj(name):
    with open(os.path.join(os.path.dirname(__file__), name + '.pkl'), 'rb') as f:
        return pickle.load(f)

# Check if tokenized sentences and embeddings already exist
if os.path.exists(os.path.join(os.path.dirname(__file__), 'corpus_sentences.pkl')) and os.path.exists(os.path.join(os.path.dirname(__file__), 'corpus_embeddings.pkl')):
    corpus_sentences = load_obj('corpus_sentences')
    corpus_embeddings = load_obj('corpus_embeddings')
else:
    # Read the text file
    with open(os.path.join(os.path.dirname(__file__), 'sseData.txt'), 'r') as f:
        corpus = f.read()

    # Tokenize the text into sentences
    spacy_tokenizer = spacy.load('en_core_web_sm')
    spacy_tokenizer.max_length = len(corpus)  # or some other large number
    corpus_sentences = [spacy_tokenizer(sentence).text.split() for sentence in corpus.split('.')]
    corpus_embeddings = model.encode([" ".join(sentence) for sentence in corpus_sentences])
    
    # Save tokenized sentences and embeddings
    save_obj(corpus_sentences, 'corpus_sentences')
    save_obj(corpus_embeddings, 'corpus_embeddings')

def get_model_and_index():
    return model, corpus_sentences, corpus_embeddings

get_model_and_index()

print('Time to generate embeddings of corpus:', round(time() - t, 4), 'seconds')
