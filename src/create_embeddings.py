from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

df = pd.read_csv("data/all_discussions.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    df["text"].tolist(),
    show_progress_bar=True
)

np.save("data/embeddings.npy", embeddings)

print("✅ Embeddings created")