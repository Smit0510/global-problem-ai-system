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

    problem = st.text_input("Enter problem")

    if st.button("Save"):
        insert_problem(problem, "Other", "", st.session_state.token, st.session_state.user)
        st.rerun()

    # AI Suggestions
    if st.button("Generate Ideas"):
        for i in generate_problems(problem):
            st.write("💡", i)

    data = get_problems(st.session_state.token)

    if data:
        for row in data:

            st.markdown(f"### 🚧 {row['problem']}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("👍", key=f"v{row['id']}"):
                    upvote_problem(row["id"], row.get("votes", 0), st.session_state.token)
                    st.rerun()

            with col2:
                if st.button("❌", key=f"d{row['id']}"):
                    delete_problem(row["id"], st.session_state.token)
                    st.rerun()

            # -------- AI BUTTONS --------
            if st.button("🚀 Startup Kit", key=f"k{row['id']}"):
                st.text(generate_startup_kit(row["problem"]))

            if st.button("🎯 Tech Stack", key=f"t{row['id']}"):
                st.text(generate_tech_stack(row["problem"]))

            if st.button("💼 Business Plan", key=f"b{row['id']}"):
                st.text(generate_business_plan(row["problem"]))

            if st.button("🎨 Landing Page Code", key=f"l{row['id']}"):
                st.code(generate_landing_page(row["problem"]), language="html")

            # -------- PDF --------
            if st.button("📄 Download PDF", key=f"p{row['id']}"):
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
                    "Download",
                    content,
                    file_name="startup_plan.txt"
                )


# ---------------- AUTH ----------------
if st.session_state.user:
    show_dashboard()
else:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = sign_in(email, password)
        if "access_token" in res:
            st.session_state.user = email
            st.session_state.token = res["access_token"]
            st.rerun()
