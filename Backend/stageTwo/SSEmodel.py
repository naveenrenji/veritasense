from .dataEmbedding import get_model_and_index
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from time import time

# Load model, index, and tokenized sentences
model, corpus_sentences, corpus_embeddings = get_model_and_index()
storage='local'

def get_SSE_results(query):
    #start time
    t = time()

    # Generate embedding for the query
    query_embedding = model.encode([query], show_progress_bar=True).tolist()[0]
    
    if storage == 'pinecone':
        # Search Pinecone index
        index='ssedata'
        res = index.query(queries=[query_embedding], top_k=20)
        matched_sentences = []
        
        if len(res['ids'][0]) > 0:
            for i, score in zip(res['ids'][0], res['scores'][0]):
                if score > 0.4:
                    matched_sentence = corpus_sentences[int(i)]
                    matched_sentences.append(matched_sentence)
                    
            concatenated_sentences = ' '.join(matched_sentences)
            return concatenated_sentences
                
        else:
            return "There was no direct match with existing sentences"
    
    elif storage == 'local':
        # Compute similarity with local embeddings
        similarity = cosine_similarity([query_embedding], corpus_embeddings)[0]
        top_k = 20
        top_k_indices = np.argsort(similarity)[-top_k:]
        top_k_similarities = similarity[top_k_indices]

        matched_sentences = []

        for j in range(top_k):
            if top_k_similarities[-j-1] > 0.5:
                sentence = ' '.join(corpus_sentences[top_k_indices[-j-1]])  # Assuming corpus_sentences is a list of lists
                matched_sentences.append(sentence)

        if len(matched_sentences) == 0:
            print('No matched sentences with a score above 0.5.')
            concatenated_sentences = 'not found'
        else:
            concatenated_sentences = ' '.join(matched_sentences)

        print('Time to evaluate the matching:', round(time() - t, 4), 'seconds')
        print('the matches sentences are : ',concatenated_sentences)

        return concatenated_sentences

# Example usage
#result = get_SSE_results("what is the difference between users and programmers")
#result = get_SSE_results("what do you think about terrosrists and murderers?")
#print("Concatenated Sentences:", result)
