import pandas as pd

rank = pd.read_csv("data/problem_rankings.csv")

rank["opportunity_score"] = (
    rank["popularity"] * 0.4 +
    rank["trend"] * 0.3 +
    rank["market_size"] * 0.2 +
    rank["uniqueness"] * 0.1
)

rank.to_csv("data/opportunity_scores.csv", index=False)

print("✅ Opportunity scores generated")