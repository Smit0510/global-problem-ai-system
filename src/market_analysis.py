import os
import pandas as pd
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


def analyze_market(problem_text):

    prompt = f"""
You are a startup market analyst.

Analyze the problem discussions and provide:

1. Market size
2. Competitors
3. Market gap
4. Startup opportunity
5. Revenue model

Discussions:
{problem_text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def run_market_analysis():

    print("Loading clustered discussions...")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # Try multiple possible filenames
    possible_files = [
        "clustered_discussions.csv",
        "discussions_clustered.csv"
    ]

    file_path = None

    for f in possible_files:
        p = os.path.join(DATA_DIR, f)
        if os.path.exists(p):
            file_path = p
            break

    if file_path is None:
        raise Exception("No clustered discussion file found in data folder")

    df = pd.read_csv(file_path)

    results = []

    for cluster_id in df["cluster"].unique():

        print(f"Analyzing cluster {cluster_id}...")

        cluster_df = df[df["cluster"] == cluster_id]

        texts = cluster_df["text"].head(10).tolist()

        combined_text = "\n".join(texts)

        analysis = analyze_market(combined_text)

        results.append({
            "cluster": cluster_id,
            "market_analysis": analysis
        })

    results_df = pd.DataFrame(results)

    output_path = os.path.join(DATA_DIR, "market_analysis.csv")

    results_df.to_csv(output_path, index=False)

    print("✅ Market analysis completed!")
    print("Saved to:", output_path)


if __name__ == "__main__":
    run_market_analysis()