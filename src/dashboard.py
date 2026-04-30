import streamlit as st
from supabase_auth import sign_up, sign_in, reset_password

st.set_page_config(page_title="AI Problem Discovery Dashboard")

# ---------------- LOGIN STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- DASHBOARD FUNCTION ----------------
def show_dashboard():

    st.title("🚀 AI Problem Discovery Dashboard")

    st.success(f"Logged in as {st.session_state.user}")

    st.markdown("---")

    # 🔥 Problems Section
    st.subheader("🔥 Trending Problems")

    problems = [
        "Managing multiple subscriptions is confusing",
        "Small businesses lack affordable marketing tools",
        "Students struggle to organize study material",
        "Freelancers have inconsistent income tracking",
    ]

    for p in problems:
        st.write(f"• {p}")

    st.markdown("---")

    # 💡 Startup Ideas Section
    st.subheader("💡 Startup Ideas")

    ideas = [
        "AI subscription manager with auto-cancel suggestions",
        "Low-cost AI marketing assistant for SMBs",
        "Smart AI study planner with summaries",
        "Freelancer income prediction dashboard",
    ]

    for i in ideas:
        st.write(f"👉 {i}")

    st.markdown("---")

    # 📊 Simple Stats
    st.subheader("📊 Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Problems Found", "24")
    col2.metric("Ideas Generated", "12")
    col3.metric("Opportunities", "5 High")

    st.markdown("---")

    # Logout
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()


# ---------------- IF USER LOGGED IN ----------------
if st.session_state.user:
    show_dashboard()


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

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):

            result = sign_in(email, password)

            if result and "access_token" in result:
                st.session_state.user = email
                st.rerun()
            else:
                st.error("Invalid email or password")

    # ---------- REGISTER ----------
    elif page == "Register":

        st.subheader("Create Account")

        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):

            result = sign_up(email, password)

            if result and "error" in result:
                st.error(result["error"])
            else:
                st.success("Account created successfully. Check your email if required.")

    # ---------- RESET PASSWORD ----------
    elif page == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input("Email", key="reset_email")

        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Password reset email sent.")
