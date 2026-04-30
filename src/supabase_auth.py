import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug (optional – remove later)
print("SUPABASE_URL:", SUPABASE_URL)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not loaded. Check environment variables.")

BASE_URL = f"{SUPABASE_URL}/auth/v1"


# ---------------- SIGN UP ----------------
def sign_up(email, password):
    try:
        res = requests.post(
            f"{BASE_URL}/signup",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "email": email,
                "password": password
            }
        )
        return res.json()

    except Exception as e:
        return {"error": str(e)}


# ---------------- SIGN IN ----------------
def sign_in(email, password):
    try:
        res = requests.post(
            f"{BASE_URL}/token?grant_type=password",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "email": email,
                "password": password
            }
        )
        return res.json()

    except Exception as e:
        return {"error": str(e)}


# ---------------- RESET PASSWORD ----------------
def reset_password(email):
    try:
        res = requests.post(
            f"{BASE_URL}/recover",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "email": email
            }
        )
        return res.json()

    except Exception as e:
        return {"error": str(e)}
