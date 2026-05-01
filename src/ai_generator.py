import os
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
            "Students struggle to stay focused while studying",
            "People find it hard to save money",
            "Freelancers struggle to find clients",
            "People forget daily tasks",
            "Beginners don't know how to start fitness"
        ]


# ---------------- CLEAN JSON ----------------
def clean_json(text):
    try:
        text = re.sub(r"```json|```", "", text).strip()
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
You are a startup founder who has built and launched real startups.

Your job is to create a PRACTICAL execution plan — not theory.

Problem:
{problem}

STRICT RULES:
- Output ONLY valid JSON
- No extra text
- No generic startup buzzwords
- Be specific (platforms, actions, numbers)
- Focus on getting FIRST 10 USERS

FORMAT:

{{
  "startup_name": "",
  "tagline": "",

  "problem_analysis": "Explain why this problem actually matters in real life",

  "solution": "Explain exactly what the product does in simple terms",

  "target_users": "Be very specific (example: college students preparing for exams)",

  "features": [
    "Real feature with purpose",
    "Another practical feature"
  ],

  "validation_plan": [
    "Post in specific communities (example: Reddit r/startups)",
    "Talk to 10 real users",
    "Ask if they will pay"
  ],

  "mvp_scope": [
    "Build only core feature",
    "Do NOT build extra features",
    "Simple UI only"
  ],

  "first_users_plan": [
    "Where to find users (Reddit, WhatsApp, Discord)",
    "How to message them directly",
    "Offer free beta access"
  ],

  "revenue_plan": "Explain how to earn first ₹1000",

  "build_steps": [
    "Step 1: Validate problem",
    "Step 2: Build MVP",
    "Step 3: Launch",
    "Step 4: Get first users"
  ],

  "tech_stack": {{
    "frontend": "",
    "backend": "",
    "database": "",
    "deployment": ""
  }},

  "go_to_market": "Step-by-step launch strategy"
}}
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        raw = res.choices[0].message.content
        return clean_json(raw)

    except Exception:
        # 🔥 STRONG FALLBACK (NO API NEEDED)
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

        return f"""{{
  "startup_name": "{name}",
  "tagline": "Solving: {problem}",
  "problem_analysis": "{problem} is a real problem people face in daily life.",
  "solution": "A focused product that directly solves this problem with simple UX.",
  "target_users": "People facing this specific problem",

  "features": [
    "Core feature solving main problem",
    "Simple tracking system",
    "User dashboard"
  ],

  "validation_plan": [
    "Post about this problem in Reddit communities",
    "Talk to 10 real users facing this issue",
    "Ask if they would pay for solution"
  ],

  "mvp_scope": [
    "Build only 1 core feature",
    "No complex UI",
    "No extra features"
  ],

  "first_users_plan": [
    "Share in WhatsApp/Telegram groups",
    "Post in niche Reddit communities",
    "Reach out to 20 people manually"
  ],

  "revenue_plan": "Charge ₹199/month after getting first users",

  "monetization": "Freemium → subscription",

  "build_steps": [
    "Validate problem",
    "Build MVP",
    "Launch simple landing page",
    "Get first 10 users"
  ],

  "tech_stack": {{
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL",
    "deployment": "Render"
  }},

  "go_to_market": "Start with communities + direct outreach"
}}"""
