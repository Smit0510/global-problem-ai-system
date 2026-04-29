import streamlit as st
import requests

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

BASE_AUTH_URL = f"{SUPABASE_URL}/auth/v1"


def sign_up(email, password):
    url = f"{BASE_AUTH_URL}/signup"
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }
    data = {"email": email, "password": password}

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def sign_in(email, password):
    url = f"{BASE_AUTH_URL}/token?grant_type=password"
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }
    data = {"email": email, "password": password}

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def reset_password(email):
    url = f"{BASE_AUTH_URL}/recover"
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }
    data = {"email": email}

    response = requests.post(url, headers=headers, json=data)
    return response.json()
