import streamlit as st
from supabase_auth import (
    sign_up, sign_in, reset_password,
    insert_problem, get_problems, delete_problem,
    upvote_problem, get_trending_problems,
    update_ai_score
)

from ai_generator import (
    generate_problems,
    generate_startup_kit,
    generate_tech_stack,
    generate_business_plan,
    generate_landing_page
)

from ai_scorer import score_problem
import re

# ✅ MUST BE FIRST
st.set_page_config(page_title="AI Startup Builder", layout="wide")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None
if "problem_input" not in st.session_state:
    st.session_state.problem_input = ""
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "Login"
if "show_password" not in st.session_state:
    st.session_state.show_password = False

# ---------------- PASSWORD STRENGTH ----------------
def password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    return score


# ---------------- DASHBOARD ----------------
def show_dashboard():

    st.title("🚀 AI Startup Builder")
    st.caption("Turn problems into startup ideas instantly")

    st.success(f"Logged in as {st.session_state.user}")

    # ---- ADD PROBLEM ----
    st.subheader("➕ Add Problem")

    problem = st.text_input(
        "Enter a real-world problem",
        value=st.session_state.problem_input
    )

    if st.button("Save Problem"):
        if not problem or len(problem.strip()) < 5:
            st.error("❌ Problem must be at least 5 characters")
        else:
            insert_problem(problem, "Other", "", st.session_state.token, st.session_state.user)
            st.success("Problem saved!")
            st.session_state.problem_input = ""
            st.rerun()

    # ---- AI SUGGESTIONS ----
    st.subheader("💡 AI Suggestions")

    if st.button("Generate Ideas"):
        ideas = generate_problems(problem if problem else "startup problems")
        for idea in ideas:
            st.markdown(f"💡 {idea}")

    # ---- LIST ----
    st.subheader("📋 Your Problems")

    data = get_problems(st.session_state.token)

    if isinstance(data, list):

        for row in data:

            st.markdown(f"""
            <div style="padding:15px; border-radius:12px; background:#1e1e1e; margin-bottom:10px">
                🚧 {row['problem']}<br>
                👍 {row.get('votes',0)}
            </div>
            """, unsafe_allow_html=True)

            # ---- SCORE ----
            ai_score = row.get("ai_score")

            if ai_score:
                st.markdown(f"🤖 Score: {ai_score}/10")
            else:
                if st.button("🧠 Score", key=row["id"]):
                    score = score_problem(row["problem"])
                    if score:
                        update_ai_score(row["id"], score, st.session_state.token)
                        st.rerun()
                    else:
                        st.error("AI failed")

            # ---- ACTIONS ----
            col1, col2 = st.columns(2)

            with col1:
                if st.button("👍", key=f"v{row['id']}"):
                    upvote_problem(row["id"], row.get("votes", 0), st.session_state.token)
                    st.rerun()

            with col2:
                if st.button("❌", key=f"d{row['id']}"):
                    delete_problem(row["id"], st.session_state.token)
                    st.rerun()

    # ---- LOGOUT ----
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()


# ---------------- AUTH UI ----------------
if not st.session_state.user:

    st.markdown("""
    <style>
    .box {
        max-width: 400px;
        margin: auto;
        padding: 30px;
        border-radius: 15px;
        background: #1e1e1e;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.title("🚀 AI Startup Builder")

    page = st.radio("", ["Login", "Register", "Reset"], horizontal=True)

    # ---------- LOGIN ----------
    if page == "Login":

        email = st.text_input("Email")

        pwd_type = "text" if st.session_state.show_password else "password"
        password = st.text_input("Password", type=pwd_type)

        st.checkbox("Show Password", key="show_password")

        if st.button("Forgot password?"):
            st.session_state.auth_page = "Reset"
            st.rerun()

        if st.button("Login"):

            if not email:
                st.error("❌ Email required")
            elif not password:
                st.error("❌ Password required")
            else:
                res = sign_in(email, password)
                if "access_token" in res:
                    st.session_state.user = email
                    st.session_state.token = res["access_token"]
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

    # ---------- REGISTER ----------
    elif page == "Register":

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        strength = password_strength(password)

        if password:
            st.progress(strength / 4)

            if strength <= 1:
                st.error("Weak password")
            elif strength == 2:
                st.warning("Medium password")
            else:
                st.success("Strong password")

        if st.button("Create Account"):

            if not email:
                st.error("❌ Email required")
            elif len(password) < 6:
                st.error("❌ Password too short")
            else:
                res = sign_up(email, password)
                if "access_token" in res:
                    st.session_state.user = email
                    st.session_state.token = res["access_token"]
                    st.rerun()
                else:
                    st.error("❌ Registration failed")

    # ---------- RESET ----------
    elif page == "Reset":

        email = st.text_input("Enter your email")

        if st.button("Send Reset Email"):
            if not email:
                st.error("❌ Enter email")
            else:
                reset_password(email)
                st.success("Email sent!")

    # ---------- GOOGLE LOGIN (INFO) ----------
    st.markdown("---")
    st.info("🔐 Google Login available via Supabase → enable OAuth in dashboard")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    show_dashboard()
