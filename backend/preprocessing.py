import pandas as pd
import re


def clean_text(text):
    text = text.strip()
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text


df = pd.read_csv("data/notes.csv")

df = df.dropna(subset=["text"])

df["cleaned_text"] = df["text"].apply(clean_text)

df.to_csv("data/cleaned_notes.csv", index=False)

print(df[["id", "text", "cleaned_text"]])