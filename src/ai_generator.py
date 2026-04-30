import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_problem(problem):

    prompt = f"""
    You are an expert startup analyst.

    Rate the following problem from 1 to 10 based on:
    - Pain level
    - Frequency
    - Market size

    IMPORTANT:
    - Return ONLY a number
    - No explanation
    - No text
    - No symbols

    Example output:
    7.5

    Problem: {problem}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2   # 🔥 more consistent output
        )

        text = response.choices[0].message.content.strip()

        print("RAW AI RESPONSE:", text)  # debug

        # 🔥 Extract number safely using regex
        match = re.search(r"\d+(\.\d+)?", text)

        if match:
            score = float(match.group())

            # clamp between 1–10
            score = max(1, min(score, 10))

            return round(score, 1)

        return None

    except Exception as e:
        print("AI ERROR:", e)
        return None
