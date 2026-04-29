import pandas as pd

def rank_problems():

    # Load clustered data
    df = pd.read_csv("data/semantic_clusters.csv")
    # Count number of discussions per cluster
    cluster_counts = df.groupby("cluster").size().reset_index(name="popularity")

    # Sort clusters by popularity
    ranked = cluster_counts.sort_values(by="popularity", ascending=False)

    # Save ranked problems
    ranked.to_csv("data/problem_rankings.csv", index=False)

    print("Problem rankings created successfully")
    print(ranked.head(10))


if __name__ == "__main__":
    rank_problems()