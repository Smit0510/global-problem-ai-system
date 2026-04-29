import streamlit as st
from supabase_auth import sign_up, sign_in, reset_password

st.set_page_config(page_title="AI Problem Discovery Dashboard")

# SESSION STATE
if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":

    st.title("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        result = sign_in(email, password)

        if "access_token" in result:
            st.session_state.user = email
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid email or password")

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create Account"):
            st.session_state.page = "register"
            st.rerun()

    with col2:
        if st.button("Forgot Password"):
            st.session_state.page = "forgot"
            st.rerun()


# ---------------- REGISTER PAGE ----------------
elif st.session_state.page == "register":

    st.title("Create Account")

    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        result = sign_up(email, password)

        if "user" in result:
            st.success("Account created successfully. Please login.")
        else:
            st.error("Registration failed")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# ---------------- FORGOT PASSWORD ----------------
elif st.session_state.page == "forgot":

    st.title("Reset Password")

    email = st.text_input("Email", key="forgot_email")

    if st.button("Send Reset Email"):
        reset_password(email)
        st.success("Password reset email sent.")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":

    st.title("AI Problem Discovery Dashboard")

    st.write("Logged in as:", st.session_state.user)

    st.write("Your AI discovery dashboard will appear here.")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
