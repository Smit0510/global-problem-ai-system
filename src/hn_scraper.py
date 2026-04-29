import requests
import pandas as pd
import time

print("Collecting Hacker News posts...")

url = "https://hacker-news.firebaseio.com/v0/topstories.json"

story_ids = requests.get(url).json()

import requests
import pandas as pd
import time

print("Collecting Hacker News posts...")

url = "https://hacker-news.firebaseio.com/v0/topstories.json"

story_ids = requests.get(url).json()

texts = []

for i, story_id in enumerate(story_ids[:1000]):
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    item = requests.get(item_url).json()

    if item and "title" in item:
        texts.append(item["title"])

    print(f"Collected {i+1} posts")

    time.sleep(0.05)

df = pd.DataFrame({"text": texts})
df.to_csv("data/news.csv", index=False)

print("\nFinished collecting posts")
print("Collected:", len(texts))
