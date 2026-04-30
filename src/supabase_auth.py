import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

AUTH_URL = f"{SUPABASE_URL}/auth/v1"
BASE_URL = f"{SUPABASE_URL}/rest/v1"


# ---------------- AUTH ----------------

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


# ---------------- DATABASE ----------------

def insert_problem(problem, category, tags, token, user_email):
    import requests

    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/problems",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        },
        json={
            "problem": problem,
            "category": category,
            "tags": tags,
            "user_email": user_email
        }
    )

    try:
        return res.json()
    except:
        return {"error": res.text}


def get_problems(token):
    res = requests.get(
        f"{BASE_URL}/problems",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}"
        }
    )

    try:
        return res.json()
    except:
        return []


# 🔥 NEW: DELETE FUNCTION
def delete_problem(problem_id, token):
    res = requests.delete(
        f"{BASE_URL}/problems?id=eq.{problem_id}",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}"
        }
    )

    return res.status_code

def upvote_problem(problem_id, current_votes, token):
    import requests

    new_votes = int(current_votes or 0) + 1

    res = requests.patch(
        f"{SUPABASE_URL}/rest/v1/problems?id=eq.{problem_id}",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"   # 🔥 IMPORTANT
        },
        json={"votes": new_votes}
    )

    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)

    return res.json()
