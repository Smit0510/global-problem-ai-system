import os
from openai import OpenAI

client = OpenAI()

def generate_problems(topic="startup problems"):
    try:
        prompt = f"""
        Generate 5 real-world problems.
        Topic: {topic}

        Rules:
        - One line each
        - No numbering
        - No explanation
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        text = response.choices[0].message.content

        problems = [
            p.strip("- ").strip()
            for p in text.split("\n")
            if len(p.strip()) > 5
        ]

        return problems

    except Exception as e:
        return [f"Error: {str(e)}"]
