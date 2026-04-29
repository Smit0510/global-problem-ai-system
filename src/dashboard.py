import streamlit as st
from supabase_auth import sign_up, sign_in, reset_password

st.set_page_config(page_title="AI Problem Discovery Dashboard")

# -------- SESSION STATE --------
if "page" not in st.session_state:
    st.session_state.page = "login"

# -------- LOGIN PAGE --------
if st.session_state.page == "login":

    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        login_btn = st.form_submit_button("Login")

        if login_btn:
            result = sign_in(email, password)

            if "access_token" in result:
                st.session_state.user = email
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid email or password")

    st.write("---")

    if st.button("Create Account"):
        st.session_state.page = "register"
        st.rerun()

    if st.button("Forgot Password"):
        st.session_state.page = "forgot"
        st.rerun()


# -------- REGISTER PAGE --------
elif st.session_state.page == "register":

    st.title("Create Account")

    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        register_btn = st.form_submit_button("Register")

        if register_btn:
            result = sign_up(email, password)

            if "user" in result:
                st.success("Account created. Please login.")
            else:
                st.error("Registration failed")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# -------- FORGOT PASSWORD --------
elif st.session_state.page == "forgot":

    st.title("Reset Password")

    with st.form("reset_form"):
        email = st.text_input("Email")

        reset_btn = st.form_submit_button("Send Reset Email")

        if reset_btn:
            reset_password(email)
            st.success("Password reset email sent.")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# -------- DASHBOARD --------
elif st.session_state.page == "dashboard":

    st.title("AI Problem Discovery Dashboard")

    st.write("Logged in as:", st.session_state.user)

    st.write("Dashboard will show AI-discovered problems here.")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
