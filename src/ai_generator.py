import os
import json
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------- PROBLEMS ----------------
def generate_problems(topic="startup problems"):
    try:
        prompt = f"""
        Generate 5 real-world startup problems.
        Topic: {topic}
        Short and realistic.
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        text = res.choices[0].message.content
        return [p.strip("- ").strip() for p in text.split("\n") if len(p.strip()) > 5]

    except:
        return [
            "People forget to pay bills on time",
            "Students struggle to stay focused",
            "Freelancers struggle to find clients",
            "People find it hard to save money",
            "Gym beginners don’t know workouts"
        ]


# ---------------- CLEAN JSON ----------------
def clean_json(text):
    try:
        # remove markdown ```json ```
        text = re.sub(r"```json|```", "", text).strip()

        # extract JSON part
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group()

        return text
    except:
        return text


# ---------------- FULL STARTUP PLAN ----------------
def generate_full_startup_plan(problem):
    try:
        prompt = f"""
        You are an expert startup advisor, product manager, and CTO.

        Given this problem:
        {problem}

        Generate a COMPLETE startup plan in STRICT JSON format:

        {{
          "startup_name": "",
          "tagline": "",
          "problem_analysis": "",
          "solution": "",
          "target_users": "",
          "features": [],
          "monetization": "",
          "build_steps": [],
          "tech_stack": {{
            "frontend": "",
            "backend": "",
            "database": "",
            "ai_tools": "",
            "deployment": ""
          }},
          "go_to_market": ""
        }}

        Rules:
        - Output ONLY JSON
        - No explanation
        - No extra text
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        raw = res.choices[0].message.content

        # clean JSON before returning
        return clean_json(raw)

    except Exception as e:
        print("AI ERROR:", e)
        return None
