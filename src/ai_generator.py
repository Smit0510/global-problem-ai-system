import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_problem(problem):

    prompt = f"""
    Rate this startup problem from 1 to 10.

    Consider:
    - Pain level
    - Frequency
    - Market size

    Only return a number.

    Problem: {problem}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        score_text = response.choices[0].message.content.strip()

        # extract number safely
        score = float(score_text.replace("/10", "").strip())

        return score

    except Exception as e:
        print("AI ERROR:", e)
        return None
