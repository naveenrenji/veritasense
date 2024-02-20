import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from time import time
import spacy

# Set the base directory to the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to load objects using pickle
def load_obj(name):
    with open(os.path.join(BASE_DIR, name + '.pkl'), 'rb') as f:
        return pickle.load(f)

# Load pre-generated data and model
def load_model_and_data():
    model_path = './models/all-roberta-large-v1'
    model = SentenceTransformer(model_path)

    corpus_sentences = load_obj('corpus_sentences')
    corpus_embeddings = load_obj('corpus_embeddings')

    return model, corpus_sentences, corpus_embeddings

# Function to get results based on sentence embeddings similarity
def get_SSE_results(query, model, corpus_sentences, corpus_embeddings):
    t = time()  # Start time

    # Generate embedding for the query
    query_embedding = model.encode([query], show_progress_bar=True).reshape(1, -1)
    
    # Compute similarity with local embeddings
    similarity = cosine_similarity(query_embedding, corpus_embeddings)[0]
    top_k = 20  # Number of top similar sentences to retrieve
    top_k_indices = np.argsort(similarity)[-top_k:]
    top_k_similarities = similarity[top_k_indices]

    matched_sentences = []

    for j in range(top_k):
        if top_k_similarities[-j-1] > 0.5:  # Threshold for similarity
            sentence = ' '.join(corpus_sentences[top_k_indices[-j-1]])
            matched_sentences.append(sentence)

    if len(matched_sentences) == 0:
        print('No matched sentences with a score above 0.5.')
        concatenated_sentences = 'not found'
    else:
        concatenated_sentences = ' '.join(matched_sentences)

    print('Time to evaluate the matching:', round(time() - t, 4), 'seconds')
    print('The matched sentences are:', concatenated_sentences)

    return concatenated_sentences

# # Example usage
# if __name__ == '__main__':
#     model, corpus_sentences, corpus_embeddings = load_model_and_data()

#     # Example queries
#     example_queries = [
#         "what is the difference between users and programmers",
#         "what do you think about terrorists and murderers?"
#     ]

#     for query in example_queries:
#         result = get_SSE_results(query, model, corpus_sentences, corpus_embeddings)
#         print("Concatenated Sentences for '{}': {}".format(query, result))
