import streamlit as st
import requests

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

BASE_URL = f"{SUPABASE_URL}/auth/v1"


def sign_up(email, password):
    res = requests.post(
        f"{BASE_URL}/signup",
        headers={"apikey": SUPABASE_KEY},
        json={"email": email, "password": password}
    )
    return res.json()


def sign_in(email, password):
    res = requests.post(
        f"{BASE_URL}/token?grant_type=password",
        headers={"apikey": SUPABASE_KEY},
        json={"email": email, "password": password}
    )
    return res.json()


def reset_password(email):
    res = requests.post(
        f"{BASE_URL}/recover",
        headers={"apikey": SUPABASE_KEY},
        json={"email": email}
    )
    return res.json()
