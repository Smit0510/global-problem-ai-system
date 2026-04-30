import os
import re
from openai import OpenAI

# safer init
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_problem(problem):

    # ❗ Check API key first
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ NO API KEY FOUND")
        return 5.0   # fallback score

    prompt = f"""
    Give ONLY a number between 1 and 10.

    Problem: {problem}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()

        print("RAW AI:", text)

        # extract number safely
        match = re.search(r"\d+(\.\d+)?", text)

        if match:
            return float(match.group())

        # ❗ fallback if weird output
        return 5.0

    except Exception as e:
        print("AI ERROR:", e)

        # ❗ fallback so app never breaks
        return 5.0
