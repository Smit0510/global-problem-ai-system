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

        raw = res.choices[0].message.content
        return clean_json(raw)

    except Exception:
        # 🔥 DYNAMIC FALLBACK (NO API)
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
  "problem_analysis": "{problem} is a common issue affecting many people.",
  "solution": "A digital platform that helps solve this problem efficiently.",
  "target_users": "People facing this problem",
  "features": ["Core feature", "Tracking", "Analytics", "User dashboard"],
  "monetization": "Freemium subscription model",
  "build_steps": ["Validate idea", "Build MVP", "Launch", "Get users"],
  "tech_stack": {{
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL",
    "ai_tools": "None",
    "deployment": "Render"
  }},
  "go_to_market": "Social media + online communities"
}}"""
