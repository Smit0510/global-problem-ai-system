import streamlit as st
from supabase_auth import (
    sign_up, sign_in, reset_password,
    insert_problem, get_problems, delete_problem,
    upvote_problem, get_trending_problems,
    update_ai_score,
    insert_profile, get_profile
)

from ai_generator import generate_problems, generate_full_startup_plan

st.set_page_config(page_title="AI Startup Builder", layout="wide")

# ---------------- SESSION ----------------
if "generated_plans" not in st.session_state:
    st.session_state.generated_plans = {}

if "build_count" not in st.session_state:
    st.session_state.build_count = 0

if "user" not in st.session_state:
    st.session_state.user = None

if "token" not in st.session_state:
    st.session_state.token = None

if "name" not in st.session_state:
    st.session_state.name = "User"

if "problem_input" not in st.session_state:
    st.session_state.problem_input = ""


# ---------------- DASHBOARD ----------------
def show_dashboard():

    st.title("🚀 AI Startup Builder")
    st.caption("Find problems → build startups")

    st.success(f"Welcome {st.session_state.name} 👋")

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

    # ---- AI IDEAS ----
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
            st.markdown(f"🏆 {row['problem']}  \n👍 {row.get('votes',0)}")

    # ---- USER PROBLEMS ----
    st.subheader("📋 Your Problems")

    data = get_problems(st.session_state.token)

    if isinstance(data, list):

        for row in data:

            st.markdown(f"---\n🚧 {row['problem']}  \n👍 {row.get('votes',0)}")

            col1, col2, col3 = st.columns(3)

            # 👍
            with col1:
                if st.button("👍", key=f"v{row['id']}"):
                    upvote_problem(row["id"], row.get("votes", 0), st.session_state.token)
                    st.rerun()

            # ❌
            with col2:
                if st.button("❌", key=f"d{row['id']}"):
                    delete_problem(row["id"], st.session_state.token)
                    st.rerun()

            # 🚀 BUILD
            with col3:
                if st.button("🚀 Build", key=f"b{row['id']}"):

                    if st.session_state.build_count >= 3:
                        st.warning("Free limit reached. Upgrade coming soon 🚀")
                    else:
                        st.session_state.generated_plans[row["id"]] = generate_full_startup_plan(row["problem"])
                        st.session_state.build_count += 1
                        st.rerun()

            # ✅ SHOW PLAN OUTSIDE BUTTON (IMPORTANT FIX)
            if row["id"] in st.session_state.generated_plans:

                import json
                plan_raw = st.session_state.generated_plans[row["id"]]

                try:
                    plan = json.loads(plan_raw)

                    st.subheader(plan["startup_name"])
                    st.caption(plan["tagline"])

                    st.write(plan["problem_analysis"])
                    st.write(plan["solution"])
                    st.write(plan["target_users"])

                    for f in plan["features"]:
                        st.write(f"• {f}")

                    if "validation_plan" in plan:
                        st.subheader("Validation Plan")
                        for v in plan["validation_plan"]:
                            st.write(f"• {v}")

                    if "first_users_plan" in plan:
                        st.subheader("First Users Plan")
                        for u in plan["first_users_plan"]:
                            st.write(f"• {u}")

                    st.write(plan.get("revenue_plan", ""))

                    for s in plan["build_steps"]:
                        st.write(f"• {s}")

                    st.json(plan["tech_stack"])
                    st.write(plan["go_to_market"])

                    # 📄 PDF (NOW ALWAYS WORKS)
                    from fpdf import FPDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, plan_raw)

                    pdf_bytes = pdf.output(dest='S').encode('latin-1')

                    st.download_button(
                        "📄 Download PDF",
                        data=pdf_bytes,
                        file_name=f"startup_{row['id']}.pdf",
                        mime="application/pdf"
                    )

                except:
                    st.write(plan_raw)

    # ---- LOGOUT ----
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.session_state.name = "User"
        st.rerun()


# ---------------- AUTH ----------------
if st.session_state.user:
    show_dashboard()

else:
    page = st.radio("Select Page", ["Login", "Register", "Reset Password"], horizontal=True)

    # LOGIN
    if page == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = sign_in(email, password)

            if "access_token" in result:
                user_id = result["user"]["id"]

                st.session_state.user = user_id
                st.session_state.token = result["access_token"]

                profile = get_profile(user_id)
                if profile:
                    st.session_state.name = f"{profile['first_name']} {profile['last_name']}"
                else:
                    st.session_state.name = "User"

                st.rerun()
            else:
                st.error("Invalid login")

    # REGISTER
    elif page == "Register":

        st.subheader("Create Account")

        col1, col2 = st.columns(2)

        with col1:
            first_name = st.text_input("First Name")

        with col2:
            last_name = st.text_input("Last Name")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):

            if not first_name or not last_name:
                st.error("Enter full name")

            elif not email or not password:
                st.error("Email & password required")

            else:
                result = sign_up(email, password)

                if "user" in result:
                    user_id = result["user"]["id"]

                    insert_profile(user_id, first_name, last_name)

                    st.success("Account created! Please login.")
                else:
                    st.error("Registration failed")

    # RESET
    elif page == "Reset Password":
        email = st.text_input("Email")

        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Email sent")
