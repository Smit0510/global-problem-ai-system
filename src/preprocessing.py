import pandas as pd
import re

# Basic list of stopwords
stopwords = {
    "the","is","are","was","were","and","or","a","an","to","of",
    "in","on","for","with","that","this","it","as","at","by","from"
}

def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    words = text.split()
    words = [word for word in words if word not in stopwords]

    return " ".join(words)


# Load dataset
df = pd.read_csv("data/news.csv")

# Apply cleaning
df["clean_text"] = df["text"].apply(clean_text)

# Save cleaned dataset
df.to_csv("data/clean_news.csv", index=False)

print("Text preprocessing completed")
print("Saved to data/clean_news.csv")