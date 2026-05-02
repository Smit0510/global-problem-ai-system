import os
import re
import json
import random

# OPTIONAL OpenAI (will auto-disable if no key)
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except:
    client = None


# ---------------- PROBLEMS ----------------
def generate_problems(topic="startup problems"):
    try:
        if not client:
            raise Exception("No API")

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
            "Students struggle to stay focused while studying",
            "People find it hard to save money",
            "Freelancers struggle to find clients",
            "People forget daily tasks",
            "Beginners don't know how to start fitness"
        ]


# ---------------- CLEAN JSON ----------------
def clean_json(text):
    try:
        text = re.sub(r"```json|```", "", text)
        text = text.replace("→", "->")

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group()

        return text.strip()
    except:
        return text


# ---------------- FALLBACK GENERATOR ----------------
def fallback_plan(problem):
    problem_lower = problem.lower()

    name = "StartupX"
    if "study" in problem_lower:
        name = "FocusFlow"
    elif "money" in problem_lower:
        name = "SaveSmart"
    elif "fitness" in problem_lower:
        name = "FitTrack"
    elif "task" in problem_lower:
        name = "TaskMate"

    score = round(random.uniform(6.5, 9.5), 1)

    data = {
        "startup_name": name,
        "tagline": f"Solving: {problem}",

        "startup_score": score,
        "market_size": "Large (Global opportunity)",
        "demand_level": random.choice(["High", "Very High", "Growing"]),
        "competition_level": random.choice(["Low", "Medium", "High"]),

        "validation_tags": [
            "High Demand",
            "Scalable",
            "Monetizable"
        ],

        "problem_analysis": f"{problem} is a real-world issue affecting many users.",
        "solution": "A simple and focused product solving this problem efficiently.",
        "target_users": "People facing this specific problem",

        "features": [
            "Core feature solving main problem",
            "Simple tracking system",
            "Clean user dashboard"
        ],

        "validation_plan": [
            "Post in Reddit communities",
            "Talk to 10 real users",
            "Ask if they would pay"
        ],

        "mvp_scope": [
            "Build only 1 core feature",
            "No complex UI",
            "No extra features"
        ],

        "first_users_plan": [
            "Share in WhatsApp/Telegram groups",
            "Post in niche communities",
            "Reach out manually"
        ],

        "revenue_plan": "Earn first ₹1000 via subscription",

        "build_steps": [
            "Validate problem",
            "Build MVP",
            "Launch product",
            "Get first users"
        ],

        "tech_stack": {
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL",
            "deployment": "Render"
        },

        "go_to_market": "Start with communities and direct outreach"
    }

    return json.dumps(data)


# ---------------- FULL STARTUP PLAN ----------------
def generate_full_startup_plan(problem):

    try:
        if not client:
            raise Exception("No API")

        prompt = f"""
You are a startup expert.

Return STRICT JSON.

Problem:
{problem}

FORMAT:
{{
  "startup_name": "",
  "tagline": "",
  "startup_score": 0,
  "problem_analysis": "",
  "solution": "",
  "target_users": "",
  "market_size": "",
  "competition_level": "",
  "demand_level": "",
  "monetization": "",
  "features": [],
  "validation_tags": []
}}
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        raw = res.choices[0].message.content
        return clean_json(raw)

    except:
        return fallback_plan(problem)
