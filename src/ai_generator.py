import os
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


# ---------------- STARTUP KIT ----------------
def generate_startup_kit(problem):
    try:
        prompt = f"""
        Problem: {problem}

        Create:
        - Startup name
        - Solution
        - Users
        - Features
        - Monetization
        - Steps to build
        Keep simple.
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content

    except:
        return "Basic startup idea generated."


# ---------------- TECH STACK ----------------
def generate_tech_stack(problem):
    try:
        prompt = f"""
        Suggest tech stack for this startup:
        {problem}

        Include:
        - Frontend
        - Backend
        - Database
        - AI tools (if needed)
        - Deployment
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content

    except:
        return "Use React, FastAPI, PostgreSQL, Deploy on Vercel."


# ---------------- BUSINESS PLAN ----------------
def generate_business_plan(problem):
    try:
        prompt = f"""
        Create a simple business plan for:
        {problem}

        Include:
        - Problem
        - Solution
        - Market
        - Revenue model
        - Go-to-market strategy
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content

    except:
        return "Basic business plan."


# ---------------- LANDING PAGE CODE ----------------
def generate_landing_page(problem):
    try:
        prompt = f"""
        Create simple HTML landing page for:
        {problem}

        Include:
        - headline
        - features
        - CTA button
        Keep it clean.
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content

    except:
        return "<h1>Startup Landing Page</h1>"
