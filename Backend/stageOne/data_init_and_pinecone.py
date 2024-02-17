import pandas as pd
import pinecone as pc
from sentence_transformers import SentenceTransformer
import spacy
import pickle
import os

# Function to save object
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# Function to load object
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
# Read the CSV file and store it in a dataframe
csv_file = os.path.join(os.path.dirname(__file__), "questions_answers.csv")
df = pd.read_csv(csv_file)

#load model
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)


# Check if tokenized questions and embeddings already exist
if os.path.exists('questions.pkl') and os.path.exists('question_embeddings.pkl'):
    questions = load_obj('questions')
    question_embeddings = load_obj('question_embeddings')
else:
    # Tokenize the questions using spacy
    spacy_tokenizer = spacy.load('en_core_web_sm')
    questions = [spacy_tokenizer(question).text for question in df['question']]
    save_obj(questions, 'questions')  # Save tokenized questions

    # Generate embeddings for the questions using model
    question_embeddings = [embedding.tolist() for embedding in model.encode(questions, show_progress_bar=True)]
    save_obj(question_embeddings, 'question_embeddings')  # Save embeddings

# Initialize Pinecone
pc.init(api_key="bfe6ce12-d327-4243-a7c0-e8a955e1b3b3", environment="us-west1-gcp-free")

# Define the index name
index_name = 'qna'

# Check if the index with the given name already exists
if index_name not in pc.list_indexes():
    # Create a Pinecone index
    #pc.create_index(name=index_name, metric="cosine", dimension=len(question_embeddings[0]))
    index = pc.Index(index_name=index_name)
    ids = [str(i) for i in range(len(question_embeddings))]
    data = list(zip(ids, question_embeddings))
    index.upsert(data)
else:
    index = pc.Index(index_name=index_name)
    ids = [str(i) for i in range(len(question_embeddings))]
    data = list(zip(ids, question_embeddings))
    index.upsert(data)

def get_model_and_index():
    return model, index, questions, df

get_model_and_index()