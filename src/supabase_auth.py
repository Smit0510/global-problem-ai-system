import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

BASE_URL = f"{SUPABASE_URL}/rest/v1"

def insert_problem(problem, token, email):
    res = requests.post(
        f"{BASE_URL}/problems",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}",  # ✅ USER TOKEN
            "Content-Type": "application/json"
        },
        json={
            "user_email": email,
            "problem": problem
        }
    )
    return res.json()


def get_problems(token):
    res = requests.get(
        f"{BASE_URL}/problems",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}"  # ✅ USER TOKEN
        }
    )
    return res.json()
