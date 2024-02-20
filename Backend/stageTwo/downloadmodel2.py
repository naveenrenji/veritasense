from sentence_transformers import SentenceTransformer

model_name = 'sentence-transformers/all-roberta-large-v1'
model = SentenceTransformer(model_name)
model.save('./models/all-roberta-large-v1')
