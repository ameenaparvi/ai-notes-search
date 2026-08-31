from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load notes
df = pd.read_csv("data/cleaned_notes.csv")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings for our notes
embeddings = model.encode(
    df["cleaned_text"].tolist(),
    convert_to_tensor=True
)


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Notes Search API is running"}


@app.post("/search")
def search(data: Question):

    # Convert user's question into an embedding
    question_embedding = model.encode(
        data.question,
        convert_to_tensor=True
    )

    # Compare question with all notes
    scores = util.cos_sim(question_embedding, embeddings)[0]

    # Find the most similar note
    best_index = scores.argmax().item()

    return {
        "question": data.question,
        "answer": df.iloc[best_index]["text"]
    }