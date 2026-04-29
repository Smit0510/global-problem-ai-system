import pandas as pd

df = pd.read_csv("data/discussions_clustered.csv")

labels = {}

for cluster in df["cluster"].unique():
    texts = df[df.cluster == cluster]["text"].head(10)

    label = " / ".join(texts.iloc[0].split()[:4])

    labels[cluster] = label

pd.DataFrame(list(labels.items()), columns=["cluster","problem_name"]) \
    .to_csv("data/problem_names.csv", index=False)

print("✅ Problem names created")