import requests
import pandas as pd


def collect_github_issues():

    url = "https://api.github.com/search/issues?q=bug+label:bug&per_page=100"

    response = requests.get(url)
    data = response.json()

    issues = []

    for item in data["items"]:

        title = item.get("title", "")
        body = item.get("body", "")

        text = f"{title} {body}"

        issues.append({
            "text": text
        })

    df = pd.DataFrame(issues)

    df.to_csv("data/github_issues.csv", index=False)

    print("GitHub issues collected:", len(df))


if __name__ == "__main__":
    collect_github_issues()