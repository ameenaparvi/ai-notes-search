import pandas as pd
from sentence_transformers import SentenceTransformer

df = pd.read_csv("data/cleaned_notes.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(df["cleaned_text"].tolist())

print("Number of notes:", len(embeddings))
print("Embedding size:", len(embeddings[0]))