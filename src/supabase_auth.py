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


# ---------------- PROFILE ----------------

def insert_profile(user_id, first_name, last_name):
    res = requests.post(
        f"{BASE_URL}/profiles",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "build_count": 0,
            "is_pro": False
        }
    )

    try:
        return res.json()
    except:
        return {"error": res.text}


def get_profile(user_id):
    res = requests.get(
        f"{BASE_URL}/profiles?id=eq.{user_id}",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
    )

    try:
        data = res.json()
        return data[0] if data else None
    except:
        return None


# ---------------- BUILD LIMIT ----------------

def get_build_data(user_id):
    res = requests.get(
        f"{BASE_URL}/profiles?id=eq.{user_id}&select=build_count,is_pro",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
    )

    try:
        data = res.json()
        return data[0] if data else {"build_count": 0, "is_pro": False}
    except:
        return {"build_count": 0, "is_pro": False}


def increment_build_count(user_id, current_count):
    new_count = (current_count or 0) + 1

    res = requests.patch(
        f"{BASE_URL}/profiles?id=eq.{user_id}",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"   # ✅ IMPORTANT FIX
        },
        json={"build_count": new_count}
    )

    print("BUILD UPDATE STATUS:", res.status_code)
    print("BUILD UPDATE RESPONSE:", res.text)

    if res.status_code in [200, 204]:
        return {"success": True}
    else:
        return {"error": res.text}


# ---------------- PROBLEMS ----------------

def insert_problem(problem, category, tags, token, user_id):
    res = requests.post(
        f"{BASE_URL}/problems",
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
            "votes": 0,
            "user_id": user_id
        }
    )

    try:
        return res.json()
    except:
        return {"error": res.text}


def get_problems(token, user_id):
    res = requests.get(
        f"{BASE_URL}/problems?user_id=eq.{user_id}",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}"
        }
    )

    try:
        return res.json()
    except:
        return []


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
    new_votes = int(current_votes or 0) + 1

    res = requests.patch(
        f"{BASE_URL}/problems?id=eq.{problem_id}",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={"votes": new_votes}
    )

    return res.json()


def get_trending_problems(token):
    res = requests.get(
        f"{BASE_URL}/problems?select=*&order=votes.desc",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}"
        }
    )

    try:
        return res.json()
    except:
        return []
