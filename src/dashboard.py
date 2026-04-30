import streamlit as st
from supabase_auth import sign_up, sign_in, reset_password

st.set_page_config(page_title="AI Problem Discovery Dashboard")

# ---------------- LOGIN STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- DASHBOARD ----------------
def show_dashboard():
    st.title("🚀 AI Problem Discovery Dashboard")
    st.success(f"Logged in as {st.session_state.user}")

    st.subheader("🔥 Trending Problems")
    st.write("• Subscription management is confusing")
    st.write("• Small businesses lack marketing tools")

    st.subheader("💡 Startup Ideas")
    st.write("👉 AI Subscription Manager")
    st.write("👉 AI Marketing Assistant")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()


# ---------------- MAIN APP ----------------
if st.session_state.user:
    show_dashboard()

else:
    page = st.radio(
        "Select Page",
        ["Login", "Register", "Reset Password"],
        horizontal=True
    )

    # ---------- LOGIN ----------
    if page == "Login":

        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            result = sign_in(email, password)

            if "access_token" in result:
                st.session_state.user = email
                st.session_state.token = result["access_token"]   # ✅ store token
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error(result.get("error_description", "Invalid email or password"))

    # ---------- REGISTER ----------
    elif page == "Register":

        st.subheader("Create Account")

        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            result = sign_up(email, password)

            if "access_token" in result:
                st.session_state.user = email
                st.success("Account created & logged in!")
                st.rerun()
            else:
                st.error(result.get("error_description", "Registration failed"))

    # ---------- RESET PASSWORD ----------
    elif page == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input("Email", key="reset_email")

        if st.button("Send Reset Email"):
            result = reset_password(email)
            st.success("Password reset email sent")
