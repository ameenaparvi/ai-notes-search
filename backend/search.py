import pandas as pd
from sentence_transformers import SentenceTransformer, util

df = pd.read_csv("data/cleaned_notes.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    df["cleaned_text"].tolist(),
    convert_to_tensor=True
)

question = input("Ask a question: ")

question_embedding = model.encode(
    question,
    convert_to_tensor=True
)

scores = util.cos_sim(question_embedding, embeddings)[0]

best_index = scores.argmax().item()

print("\nMost relevant note:")
print(df.iloc[best_index]["text"])