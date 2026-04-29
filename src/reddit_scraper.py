import praw
import pandas as pd

# Reddit API credentials (temporary public access)
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="problem_discovery_ai"
)

subreddits = [
    "startups",
    "entrepreneur",
    "technology",
    "programming"
]

posts = []

for subreddit in subreddits:

    for submission in reddit.subreddit(subreddit).hot(limit=100):

        posts.append({
            "text": submission.title
        })

df = pd.DataFrame(posts)

df.to_csv("data/reddit_posts.csv", index=False)

print("Reddit posts saved")