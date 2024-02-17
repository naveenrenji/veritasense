import pandas as pd
import pinecone as pc
from sentence_transformers import SentenceTransformer
import spacy

# Read the CSV file and store it in a dataframe
csv_file = "questions_answers.csv"
df = pd.read_csv(csv_file)

# Tokenize the questions using spacy
spacy_tokenizer = spacy.load('en_core_web_sm')
questions = [spacy_tokenizer(question).text for question in df['question']]

# Generate embeddings for the questions using a roberta model
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)
question_embeddings = [embedding.tolist() for embedding in model.encode(questions, show_progress_bar=True)]

# Initialize Pinecone
pc.init(api_key="bfe6ce12-d327-4243-a7c0-e8a955e1b3b3", environment="us-west1-gcp-free")

# Define the index name
index_name = 'qna'

# Check if the index with the given name already exists
if index_name not in pc.list_indexes():
    # Create a Pinecone index
    #pc.create_index(name=index_name, metric="cosine", dimension=len(question_embeddings[0]))
    index = pc.Index(index_name=index_name)

    # Add the question embeddings to the Pinecone index
    ids = [str(i) for i in range(len(question_embeddings))]
    data = list(zip(ids, question_embeddings))
    index.upsert(data)
else:
    index = pc.Index(index_name=index_name)

# Function to query the Pinecone index and retrieve the answer
def get_answer(query):
    while True:
        #query = input("You: ")
        query_embedding = model.encode([query], show_progress_bar=True).tolist()[0] # Get the first element
        res = index.query(vector=query_embedding, top_k=1, include_values=True)
        if len(res.matches)>0:
            match = res.matches[0]
            matched_question = questions[int(match.id)] # Update matched_question here
            if match.score > 0.7:
                answer = df['answer'][int(match.id)]
                print(f"Query: {query} || Matched question: {matched_question} || Answer: {answer} ||")
                return answer
        else:
            print(f"There was no direct match with existing questions")
            #The closest match was : {matched_question} || \n with a score of  : {match.score} ")
            return ''
# Example 
# Can I present my code on jupyter notebook for the presentation?
# Can I please have the EM 624 midterm scheduled to a different time as well?
# My outlook isnt working, can i send through canvas?
#get_answer()


# Deinitialize Pinecone
#pc.deinit()
