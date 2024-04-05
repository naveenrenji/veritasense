# main_application.py

import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer
import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Functions to load objects using pickle
def load_obj(name):
    with open(os.path.join(os.path.dirname(__file__), name + '.pkl'), 'rb') as f:
        return pickle.load(f)

# Load pre-generated data and model
def load_data2():
    questions = load_obj('questions')
    question_embeddings = np.array(load_obj('question_embeddings'))
    csv_file = os.path.join(os.path.dirname(__file__), "qna.csv")
    df = pd.read_csv(csv_file)

    model_path = './models/all-roberta-large-v1' 
    model = SentenceTransformer(model_path)

    return model, question_embeddings, questions, df

# Function to get the closest answer to a query
def get_answer2(query, model, question_embeddings, questions, df):
    query_embedding = model.encode([query], show_progress_bar=False).reshape(1, -1)
    similarities = cosine_similarity(query_embedding, question_embeddings)[0]
    closest_idx = similarities.argmax()

    if similarities[closest_idx] > 0.5:
        matched_question = questions[closest_idx]
        answer = df['answer'][closest_idx]
        print(f"Query: {query} || Matched question: {matched_question}   navs || Answer: {answer} ||")
        #return answer
    else:
        print("There was no direct match with existing questions.")
        return 'not found'

# # Example usage
# if __name__ == '__main__':
#     model, question_embeddings, questions, df = load_data()
#     # Example queries
#     example_queries = [
#         "how to install jupyter",
#         "Can I present my code on jupyter notebook for the presentation?",
#         "Can I please have the EM 624 midterm scheduled to a different time as well?",
#         "My outlook isn't working, can I send through canvas?"
#     ]

#     for query in example_queries:
#         get_answer(query, model, question_embeddings, questions, df)

# query="how to merge pandas"
# stageTwoModel, question_embeddings, questions, df = load_data2()
# context = get_answer2(query, stageTwoModel, question_embeddings, questions, df)
# print(context)