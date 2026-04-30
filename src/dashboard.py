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

# ✅ MUST BE FIRST
st.set_page_config(page_title="AI Startup Builder", layout="wide")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None
if "problem_input" not in st.session_state:
    st.session_state.problem_input = ""

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
        if problem and len(problem.strip()) > 5:
            insert_problem(
                problem.strip(),
                "Other",
                "",
                st.session_state.token,
                st.session_state.user
            )
            st.success("Problem saved!")
            st.session_state.problem_input = ""
            st.rerun()
        else:
            st.warning("Enter a meaningful problem")

    # ---- AI SUGGESTIONS ----
    st.subheader("💡 AI Suggestions")

    if st.button("Generate Ideas"):
        ideas = generate_problems(problem if problem else "startup problems")
        for idea in ideas:
            st.markdown(f"💡 {idea}")

    # ---- TRENDING ----
    st.subheader("🔥 Trending Problems")

    trending = get_trending_problems(st.session_state.token)

    if isinstance(trending, list) and len(trending) > 0:
        for row in trending[:5]:
            st.markdown(f"""
            <div style="padding:10px; border-radius:10px; background:#262626; margin-bottom:10px">
                🏆 <b>{row['problem']}</b><br>
                👍 Votes: {row.get('votes',0)}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No trending data yet")

    # ---- BEST IDEAS ----
    st.subheader("🏆 Best Startup Ideas")

    data = get_problems(st.session_state.token)

    if isinstance(data, list) and len(data) > 0:

        def rank(row):
            return (row.get("ai_score", 0) * 2) + row.get("votes", 0)

        top = sorted(data, key=rank, reverse=True)[:5]

        for row in top:
            st.markdown(f"""
            <div style="padding:12px; border-radius:12px; background:#2a2a2a; margin-bottom:10px">
                🚀 <b>{row['problem']}</b><br><br>
                🤖 Score: {row.get('ai_score',0)} | 👍 Votes: {row.get('votes',0)}
            </div>
            """, unsafe_allow_html=True)

    # ---- SEARCH ----
    st.subheader("🔍 Search")

    search = st.text_input("Search problems")

    # ---- LIST ----
    st.subheader("📋 Your Problems")

    if isinstance(data, list) and len(data) > 0:

        for row in data:

            if search and search.lower() not in row["problem"].lower():
                continue

            st.markdown(f"""
            <div style="padding:15px; border-radius:12px; background:#1e1e1e; margin-bottom:10px">
                🚧 {row['problem']}<br><br>
                👍 Votes: {row.get('votes',0)}
            </div>
            """, unsafe_allow_html=True)

            # ---- AI SCORE ----
            ai_score = row.get("ai_score")

            if ai_score:
                st.markdown(f"🤖 AI Score: **{ai_score}/10**")
            else:
                if st.button("🧠 Score", key=f"s{row['id']}"):
                    score = score_problem(row["problem"])
                    if score:
                        update_ai_score(row["id"], score, st.session_state.token)
                        st.rerun()
                    else:
                        st.error("AI scoring failed")

            # ---- ACTIONS ----
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("👍", key=f"v{row['id']}"):
                    upvote_problem(row["id"], row.get("votes", 0), st.session_state.token)
                    st.rerun()

            with col2:
                if st.button("❌", key=f"d{row['id']}"):
                    delete_problem(row["id"], st.session_state.token)
                    st.rerun()

            with col3:
                if st.button("🚀 Build", key=f"b{row['id']}"):
                    st.session_state[f"build_{row['id']}"] = True

            # ---- BUILD PANEL ----
            if st.session_state.get(f"build_{row['id']}"):

                st.markdown("### 🚀 Startup Kit")
                st.text(generate_startup_kit(row["problem"]))

                st.markdown("### 🎯 Tech Stack")
                st.text(generate_tech_stack(row["problem"]))

                st.markdown("### 💼 Business Plan")
                st.text(generate_business_plan(row["problem"]))

                st.markdown("### 🎨 Landing Page")
                st.code(generate_landing_page(row["problem"]), language="html")

                # ---- DOWNLOAD ----
                content = f"""
Problem:
{row['problem']}

Startup Kit:
{generate_startup_kit(row['problem'])}

Tech Stack:
{generate_tech_stack(row['problem'])}

Business Plan:
{generate_business_plan(row['problem'])}
"""
                st.download_button(
                    "📄 Download Plan",
                    content,
                    file_name="startup_plan.txt"
                )

    else:
        st.info("No problems yet")

    # ---- LOGOUT ----
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()


# ---------------- AUTH (STYLED LOGIN) ----------------
if not st.session_state.user:

    st.markdown("""
    <style>
    .login-box {
        max-width: 400px;
        margin: auto;
        padding: 30px;
        border-radius: 15px;
        background: #1e1e1e;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }
    .title {
        text-align: center;
        font-size: 28px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="title">🚀 AI Startup Builder</div>', unsafe_allow_html=True)

    page = st.radio("", ["Login", "Register", "Reset"], horizontal=True)

    if page == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = sign_in(email, password)
            if "access_token" in res:
                st.session_state.user = email
                st.session_state.token = res["access_token"]
                st.rerun()
            else:
                st.error("Invalid login")

    elif page == "Register":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            res = sign_up(email, password)
            if "access_token" in res:
                st.session_state.user = email
                st.session_state.token = res["access_token"]
                st.rerun()
            else:
                st.error("Registration failed")

    elif page == "Reset":
        email = st.text_input("Email")

        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Email sent")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    show_dashboard()
