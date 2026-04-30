import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

AUTH_URL = f"{SUPABASE_URL}/auth/v1"
BASE_URL = f"{SUPABASE_URL}/rest/v1"


def sign_up(email, password):
    res = requests.post(
        f"{AUTH_URL}/signup",
        headers={"apikey": SUPABASE_KEY},
        json={"email": email, "password": password}
    )
    return res.json()


def sign_in(email, password):
    res = requests.post(
        f"{AUTH_URL}/token?grant_type=password",
        headers={"apikey": SUPABASE_KEY},
        json={"email": email, "password": password}
    )
    return res.json()


def reset_password(email):
    res = requests.post(
        f"{AUTH_URL}/recover",
        headers={"apikey": SUPABASE_KEY},
        json={"email": email}
    )
    return res.json()


# -------- DATABASE --------

def insert_problem(problem, token, email):
    res = requests.post(
        f"{BASE_URL}/problems",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}",
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
            "Authorization": f"Bearer {token}"
        }
    )
    return res.json()
