import os
import random

# Try OpenAI (optional)
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    USE_AI = True
except:
    USE_AI = False


def generate_problems(topic="startup problems"):

    # ---------- TRY REAL AI ----------
    if USE_AI:
        try:
            prompt = f"""
            Generate 5 real-world problems.
            Topic: {topic}

            Rules:
            - Short (1 sentence)
            - Realistic
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.choices[0].message.content

            problems = text.split("\n")

            clean = [
                p.strip("- ").strip()
                for p in problems
                if len(p.strip()) > 5
            ]

            if len(clean) > 0:
                return clean

        except Exception as e:
            print("AI failed, using fallback:", e)

    # ---------- FALLBACK (FREE) ----------
    sample_problems = [
        "People forget to pay bills on time",
        "Students struggle to stay focused while studying",
        "Small businesses don’t know how to market online",
        "Freelancers struggle to find consistent clients",
        "People waste too much time on social media",
        "Gym beginners don’t know what workout to follow",
        "Startups fail to validate ideas early",
        "People find it hard to save money",
        "Remote workers feel isolated and unproductive",
        "Users forget passwords and get locked out often"
    ]

    return random.sample(sample_problems, 5)
