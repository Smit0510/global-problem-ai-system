import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------- SIGN UP --------
def sign_up(email, password):
    try:
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )
        return response
    except Exception as e:
        return {"error": str(e)}


# -------- SIGN IN --------
def sign_in(email, password):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )
        return response
    except Exception as e:
        return {"error": str(e)}


# -------- RESET PASSWORD --------
def reset_password(email):
    try:
        supabase.auth.reset_password_email(email)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
