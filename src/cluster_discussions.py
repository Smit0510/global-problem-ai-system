import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_discussions():

    # Load merged discussions
    df = pd.read_csv("data/all_discussions.csv")

    texts = df["text"].fillna("")

    # Convert text to vectors
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    X = vectorizer.fit_transform(texts)

    # Create clusters
    kmeans = KMeans(n_clusters=5, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)

    # Save clustered dataset
    df.to_csv("data/clustered_discussions.csv", index=False)

    print("Clustering complete.")
    print(df["cluster"].value_counts())


if __name__ == "__main__":
    cluster_discussions()