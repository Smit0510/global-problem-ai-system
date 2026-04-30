import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_problems(topic="startup problems"):

    prompt = f"""
    Generate 5 real-world startup problems.

    Topic: {topic}

    Rules:
    - Short (1 sentence each)
    - Realistic
    - Painful problems people face
    - Do NOT number them
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        text = response.choices[0].message.content

        print("RAW AI:", text)  # debug

        # split lines safely
        lines = text.split("\n")

        problems = []
        for line in lines:
            clean = line.strip("- ").strip()
            if len(clean) > 10:
                problems.append(clean)

        return problems

    except Exception as e:
        print("AI ERROR:", e)
        return ["Error generating ideas"]
