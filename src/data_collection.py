import requests
import pandas as pd

# Hacker News API
url = "https://hn.algolia.com/api/v1/search?query=technology"

response = requests.get(url)
data = response.json()

titles = []

for item in data["hits"]:
    if item["title"]:
        titles.append(item["title"])

# Convert to DataFrame
df = pd.DataFrame(titles, columns=["text"])

# Save dataset
df.to_csv("data/news.csv", index=False)

print("Data collected and saved!")