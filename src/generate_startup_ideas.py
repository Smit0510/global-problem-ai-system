import pandas as pd
import ollama


def generate_ideas():

    print("Loading clustered discussions...")

    df = pd.read_csv("data/semantic_clusters.csv")

    clusters = df.groupby("cluster")["text"].apply(list)

    results = []

    for cluster_id, texts in clusters.items():

        sample = "\n".join(texts[:10])

        prompt = f"""
        You are a startup analyst.

        Below are discussions from developers and tech communities.

        Your job is to identify a REAL problem that could become a startup.

        Discussions:
        {sample}

        Return your answer in this format:

        Problem:
        (short description)

        Startup Idea:
        (a specific product solving it)

        Target Users:
        (who would pay)

        Revenue Model:
        (how the startup makes money)

        Keep answers short and practical.
        """

        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        idea = response["message"]["content"]

        results.append({
            "cluster": cluster_id,
            "idea": idea
        })

    ideas_df = pd.DataFrame(results)

    ideas_df.to_csv("data/startup_ideas.csv", index=False)

    print("Startup ideas generated!")
    print(ideas_df)


if __name__ == "__main__":
    generate_ideas()