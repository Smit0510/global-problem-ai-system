import pandas as pd

df = pd.read_csv("data/discussions_clustered.csv")

trend = (
    df.groupby(["cluster","date"])
    .size()
    .reset_index(name="count")
)

trend.to_csv("data/trend_scores.csv", index=False)

print("✅ Trend analysis created")