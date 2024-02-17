from stageOne.data_init_and_pinecone import get_model_and_index

model, index, questions, df = get_model_and_index()

def get_answer(query):
        query_embedding = model.encode([query], show_progress_bar=True).tolist()[0]
        res = index.query(vector=query_embedding, top_k=1, include_values=True)
        if len(res.matches) > 0:
            match = res.matches[0]
            matched_question = questions[int(match.id)]
            if match.score > 0.5:
                answer = df['answer'][int(match.id)]
                print(f"Query: {query} || Matched question: {matched_question} || Answer: {answer} ||")
                return answer
            else:
                print(f"There was no direct match with existing questions")
                return 'not found'

        else:
            print(f"There was no direct match with existing questions")
            return 'not found'


# Example 
# Can I present my code on jupyter notebook for the presentation?
# Can I please have the EM 624 midterm scheduled to a different time as well?
# My outlook isnt working, can i send through canvas?
#get_answer("how to install jupyter")