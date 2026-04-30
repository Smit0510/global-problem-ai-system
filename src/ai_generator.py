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
        You are an expert startup advisor.

        Problem:
        {problem}

        Return ONLY valid JSON:

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
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        return res.choices[0].message.content

    except Exception as e:

        # 🔥 FREE FALLBACK (NO API)
        return f"""{{
          "startup_name": "FocusFlow",
          "tagline": "Stay focused, achieve more",
          "problem_analysis": "People struggle to stay focused due to distractions and lack of structured workflow.",
          "solution": "An app that blocks distractions and provides structured work sessions.",
          "target_users": "Students, remote workers, freelancers",
          "features": ["Focus timer", "Distraction blocker", "Daily goals", "Progress tracking"],
          "monetization": "Freemium model with premium productivity tools",
          "build_steps": ["Validate idea", "Build MVP", "Launch landing page", "Get first users"],
          "tech_stack": {{
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL",
            "ai_tools": "None",
            "deployment": "Vercel + Render"
          }},
          "go_to_market": "Launch on social media and student communities"
        }}"""
