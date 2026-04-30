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
    st.caption("Find problems → build startups")

    st.success(f"Logged in as {st.session_state.user}")

    # ---- ADD PROBLEM ----
    st.subheader("➕ Add Problem")

    problem = st.text_input(
        "Enter a real-world problem",
        value=st.session_state.problem_input
    )

    if st.button("Save Problem"):
        if problem and len(problem.strip()) > 5:
            insert_problem(problem, "Other", "", st.session_state.token, st.session_state.user)
            st.success("Saved!")
            st.session_state.problem_input = ""
            st.rerun()
        else:
            st.error("Enter valid problem")

    # ---- AI SUGGESTIONS ----
    st.subheader("💡 AI Suggestions")

    if st.button("Generate Ideas"):
        ideas = generate_problems(problem if problem else "startup problems")
        for idea in ideas:
            st.markdown(f"💡 {idea}")

    # ---- TRENDING ----
    st.subheader("🔥 Trending")

    trending = get_trending_problems(st.session_state.token)

    if isinstance(trending, list):
        for row in trending[:5]:
            st.markdown(f"""
            🏆 {row['problem']}  
            👍 {row.get('votes',0)}  
            """)

    # ---- BEST IDEAS ----
    st.subheader("🏆 Best Startup Ideas")

    data = get_problems(st.session_state.token)

    if isinstance(data, list):

        def rank(row):
            return (row.get("ai_score", 0) * 2) + row.get("votes", 0)

        best = sorted(data, key=rank, reverse=True)[:5]

        for row in best:
            st.markdown(f"""
            🚀 {row['problem']}  
            🤖 {row.get('ai_score',0)} | 👍 {row.get('votes',0)}
            """)

    # ---- SEARCH ----
    st.subheader("🔍 Search & Filter")

    search = st.text_input("Search")

    # ---- LIST ----
    st.subheader("📋 Your Problems")

    if isinstance(data, list):

        for row in data:

            if search and search.lower() not in row["problem"].lower():
                continue

            st.markdown(f"""
            ---
            🚧 {row['problem']}  
            👍 {row.get('votes',0)}
            """)

            # ---- AI SCORE ----
            if row.get("ai_score"):
                st.write(f"🤖 Score: {row['ai_score']}")
            else:
                if st.button("Score", key=f"s{row['id']}"):
                    score = score_problem(row["problem"])
                    if score:
                        update_ai_score(row["id"], score, st.session_state.token)
                        st.rerun()
                    else:
                        st.error("AI failed")

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

                    st.info("Generating startup...")

                    st.subheader("📦 Startup Kit")
                    st.write(generate_startup_kit(row["problem"]))

                    st.subheader("🛠 Tech Stack")
                    st.write(generate_tech_stack(row["problem"]))

                    st.subheader("💼 Business Plan")
                    st.write(generate_business_plan(row["problem"]))

                    st.subheader("🌐 Landing Page")
                    st.code(generate_landing_page(row["problem"]))

    # ---- LOGOUT ----
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()


# ---------------- AUTH (UNCHANGED) ----------------
if st.session_state.user:
    show_dashboard()

else:
    page = st.radio(
        "Select Page",
        ["Login", "Register", "Reset Password"],
        horizontal=True
    )

    if page == "Login":

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = sign_in(email, password)

            if "access_token" in result:
                st.session_state.user = email
                st.session_state.token = result["access_token"]
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid login")

    elif page == "Register":

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            result = sign_up(email, password)

            if "access_token" in result:
                st.session_state.user = email
                st.session_state.token = result["access_token"]
                st.success("Account created!")
                st.rerun()
            else:
                st.error("Registration failed")

    elif page == "Reset Password":

        email = st.text_input("Email")

        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Email sent")
