import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_problems(topic="startup problems"):
    try:
        prompt = f"""
        Generate 5 real-world startup problems.
        Topic: {topic}

        Rules:
        - Short (1 sentence)
        - Realistic
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        text = res.choices[0].message.content
        return [p.strip("- ").strip() for p in text.split("\n") if len(p.strip()) > 5]

    except:
        # fallback (no API)
        return [
            "People forget to pay bills on time",
            "Students struggle to stay focused while studying",
            "Freelancers struggle to find consistent clients",
            "People find it hard to save money",
            "Gym beginners don’t know what workout to follow"
        ]


# 🔥 NEW FEATURE
def generate_startup_kit(problem):

    try:
        prompt = f"""
        Based on this problem:

        {problem}

        Generate:
        1. Landing page headline (1 line)
        2. Short product description (2 lines)
        3. Investor pitch (3 lines)
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content

    except:
        return f"""
🚀 Landing Page:
Solve: {problem}

📱 App Description:
An app designed to solve this problem effectively.

💼 Pitch:
We are building a solution for {problem} with strong market demand.
"""
