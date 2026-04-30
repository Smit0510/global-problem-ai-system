import os
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_problems(topic="startup problems"):
    try:
        prompt = f"""
        Generate 5 real-world startup problems.

        Topic: {topic}

        Rules:
        - One line each
        - No numbering
        - No explanations
        - Just plain problems
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        text = response.choices[0].message.content

        # Clean output
        problems = text.split("\n")

        clean_problems = [
            p.replace("-", "").strip()
            for p in problems
            if len(p.strip()) > 5
        ]

        return clean_problems

    except Exception as e:
        return [f"Error: {str(e)}"]
