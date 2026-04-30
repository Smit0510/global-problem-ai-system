import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_problem(problem):

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

        # extract number safely
        match = re.search(r"\d+(\.\d+)?", text)

        if match:
            return float(match.group())

        return None

    except Exception as e:
        print("AI ERROR:", e)
        return None
