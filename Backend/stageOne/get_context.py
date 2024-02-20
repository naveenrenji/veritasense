import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer
import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Functions to save and load objects using pickle
def save_obj(obj, name):
    with open(os.path.join(os.path.dirname(__file__), name + '.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(os.path.join(os.path.dirname(__file__), name + '.pkl'), 'rb') as f:
        print("here")
        return pickle.load(f)

# Function to initialize and prepare data
def init_data():
    csv_file = os.path.join(os.path.dirname(__file__), "questions_answers.csv")
    df = pd.read_csv(csv_file)
    print("here")

    # model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    # model = SentenceTransformer(model_name)

    model_path = './models/all-MiniLM-L6-v2'  
    model = SentenceTransformer(model_path)


    if os.path.exists('questions.pkl') and os.path.exists('question_embeddings.pkl'):
        questions = load_obj('questions')
        question_embeddings = np.array(load_obj('question_embeddings'))
        print("here")
    else:
        spacy_tokenizer = spacy.load('en_core_web_sm')
        questions = [spacy_tokenizer(question).text for question in df['question']]
        save_obj(questions, 'questions')

        question_embeddings = np.array(model.encode(questions, show_progress_bar=True))
        save_obj(question_embeddings, 'question_embeddings')

    return model, question_embeddings, questions, df

# Function to get the closest answer to a query
def get_answer(query, model, question_embeddings, questions, df):
    # Generate the query embedding and ensure it is 2D
    query_embedding = model.encode([query], show_progress_bar=False).reshape(1, -1)
    
    # Compute cosine similarity
    similarities = cosine_similarity(query_embedding, question_embeddings)[0]
    closest_idx = similarities.argmax()

    if similarities[closest_idx] > 0.5:
        matched_question = questions[closest_idx]
        answer = df['answer'][closest_idx]
        print(f"Query: {query} || Matched question: {matched_question}   navs || Answer: {answer} ||")
        return answer
    else:
        print("There was no direct match with existing questions.")
        return 'not found'

# Main function to run the script only for me when I am debugging
if __name__ == '__main__':
    model, question_embeddings, questions, df = init_data()

    # Example queries
    example_queries = [
        "how to install jupyter",
        "Can I present my code on jupyter notebook for the presentation?",
        "Can I please have the EM 624 midterm scheduled to a different time as well?",
        "My outlook isn't working, can I send through canvas?"
    ]

    for query in example_queries:
        get_answer(query, model, question_embeddings, questions, df)
