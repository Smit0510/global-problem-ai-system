import streamlit as st

# ✅ MUST BE FIRST
st.set_page_config(page_title="AI Problem Dashboard")

# 🎨 CUSTOM UI STYLE
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.3);
}

.stButton>button {
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 500;
}

h1, h2, h3 {
    color: #ffffff;
}

p, span, div {
    color: #d1d5db;
}
</style>
""", unsafe_allow_html=True)


from supabase_auth import (
    sign_up,
    sign_in,
    reset_password,
    insert_problem,
    get_problems,
    delete_problem,
)

from ai_generator import generate_problems


# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "token" not in st.session_state:
    st.session_state.token = None

if "problem_input" not in st.session_state:
    st.session_state.problem_input = ""


# ---------------- DASHBOARD ----------------
def show_dashboard():

    # 🎯 HEADER
    st.markdown("""
    <h1 style='text-align: center;'>🚀 AI Problem Discovery</h1>
    <p style='text-align: center; color: gray;'>Find real-world problems & build startups</p>
    """, unsafe_allow_html=True)

    st.success(f"Logged in as {st.session_state.user}")

    st.markdown("###")

    # -------- ADD PROBLEM --------
    st.subheader("➕ Add Problem")

    problem = st.text_input(
        "Enter a real-world problem",
        value=st.session_state.problem_input
    )

    col1, col2 = st.columns([2, 1])

    # ---- SAVE ----
    with col1:
        if st.button("💾 Save Problem"):

            if problem and len(problem.strip()) > 5:

                insert_problem(
                    problem.strip(),
                    st.session_state.token,
                    st.session_state.user
                )

                st.success("Problem saved!")
                st.session_state.problem_input = ""
                st.rerun()

            else:
                st.warning("Enter meaningful problem")

    # ---- AI GENERATE ----
    with col2:
        if st.button("🤖 Suggest Problems"):
            st.session_state.ai_problems = generate_problems("startup")

    st.markdown("###")

    # -------- AI SUGGESTIONS --------
    if "ai_problems" in st.session_state:

        st.subheader("💡 AI Suggestions")

        for i, p in enumerate(st.session_state.ai_problems):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"""
                <div class="card">
                    💡 {p}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button("Use", key=f"use_{i}"):
                    st.session_state.problem_input = p
                    st.rerun()

    st.markdown("---")

    # -------- SHOW PROBLEMS --------
    st.subheader("📋 Your Problems")

    data = get_problems(st.session_state.token)

    if isinstance(data, list) and len(data) > 0:

        for row in data:
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"""
                <div class="card">
                    🚧 {row['problem']}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button("❌", key=row["id"]):
                    delete_problem(row["id"], st.session_state.token)
                    st.rerun()

    else:
        st.info("No problems yet")

    st.markdown("---")

    # -------- LOGOUT --------
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()


# ---------------- AUTH ----------------
if st.session_state.user:
    show_dashboard()

else:
    page = st.radio(
        "Select Page",
        ["Login", "Register", "Reset Password"],
        horizontal=True
    )

    # -------- LOGIN --------
    if page == "Login":

        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):

            result = sign_in(email, password)

            if "access_token" in result:
                st.session_state.user = email
                st.session_state.token = result["access_token"]
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error(result.get("error_description", "Invalid email or password"))

    # -------- REGISTER --------
    elif page == "Register":

        st.subheader("Create Account")

        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):

            result = sign_up(email, password)

            if "access_token" in result:
                st.session_state.user = email
                st.session_state.token = result["access_token"]
                st.success("Account created & logged in!")
                st.rerun()
            else:
                st.error(result.get("error_description", "Registration failed"))

    # -------- RESET PASSWORD ----------
    elif page == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input("Email", key="reset_email")

        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Password reset email sent")
