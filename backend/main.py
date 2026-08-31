from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
vectorizer = TfidfVectorizer()
embeddings = vectorizer.fit_transform(df["cleaned_text"])
# Load embedding model



class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Notes Search API is running"}


@app.post("/search")
def search(data: Question):

    # Convert question into TF-IDF vector
    question_vector = vectorizer.transform([data.question])

    # Compare question with all notes
    scores = cosine_similarity(question_vector, embeddings)[0]

    # Find most similar note
    best_index = scores.argmax()

    return {
        "question": data.question,
        "answer": df.iloc[best_index]["text"]
    }
