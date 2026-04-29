import streamlit as st
from supabase_auth import sign_up, sign_in, reset_password

st.set_page_config(page_title="AI Problem Discovery Dashboard")

# ---------------- LOGIN STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- IF USER LOGGED IN ----------------
if st.session_state.user:

    st.title("AI Problem Discovery Dashboard")
    st.success(f"Logged in as {st.session_state.user}")

    st.write("Your AI-discovered startup problems will appear here.")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ---------------- AUTH PAGES ----------------
else:

    page = st.radio(
        "Select Page",
        ["Login", "Register", "Reset Password"],
        horizontal=True
    )

    # ---------- LOGIN ----------
    if page == "Login":

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            result = sign_in(email, password)

            if "access_token" in result:
                st.session_state.user = email
                st.rerun()
            else:
                st.error("Invalid email or password")

    # ---------- REGISTER ----------
    elif page == "Register":

        st.subheader("Create Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):

            result = sign_up(email, password)

            if "user" in result:
                st.success("Account created successfully. You can now login.")
            else:
                st.error("Registration failed")

    # ---------- RESET PASSWORD ----------
    elif page == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input("Email")

        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Password reset email sent.")
