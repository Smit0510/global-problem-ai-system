import streamlit as st
import requests
import os

from supabase_auth import (
    sign_up, sign_in, reset_password,
    insert_problem, get_problems, delete_problem,
    upvote_problem, get_trending_problems,
    insert_profile, get_profile,
    get_build_data, increment_build_count
)

from ai_generator import generate_problems, generate_full_startup_plan

st.set_page_config(page_title="AI Startup Builder", layout="wide")

# ---------------- SESSION ----------------
if "generated_plans" not in st.session_state:
    st.session_state.generated_plans = {}

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

    # ✅ BUILD DATA
    user_data = get_build_data(
        st.session_state.user,
        st.session_state.token
    )

    build_count = user_data.get("build_count", 0)
    is_pro = user_data.get("is_pro", False)

    st.info(f"🧠 Builds used: {build_count}/3")

    # ---- ADD PROBLEM ----
    st.subheader("➕ Add Problem")

    problem = st.text_input(
        "Enter a real-world problem",
        value=st.session_state.problem_input
    )

    if st.button("Save Problem"):

        if not st.session_state.user:
            st.error("User not logged in properly")
            return

        if problem and len(problem.strip()) > 5:

            insert_problem(
                problem,
                "Other",
                "",
                st.session_state.token,
                st.session_state.user
            )

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
            st.markdown(f"🏆 {row['problem']}  \n👍 {row.get('votes', 0)}")

    # ---- USER PROBLEMS ----
    st.subheader("📋 Your Problems")

    data = get_problems(st.session_state.token, st.session_state.user)

    if isinstance(data, list) and len(data) > 0:

        for row in data:

            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:10px;
                border:1px solid #ddd;
                margin-bottom:10px;
                background-color:#fafafa;
            ">
                <b>🚧 {row['problem']}</b><br>
                👍 {row.get('votes', 0)} votes
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            # 👍 UPVOTE
            with col1:
                if st.button("👍 Upvote", key=f"v{row['id']}"):
                    upvote_problem(row["id"], row.get("votes", 0), st.session_state.token)
                    st.rerun()

            # ❌ DELETE
            with col2:
                if st.button("❌ Delete", key=f"d{row['id']}"):
                    delete_problem(row["id"], st.session_state.token)
                    st.rerun()

            # 🚀 BUILD (FIXED)
            with col3:
                if st.button("🚀 Build Startup", key=f"b{row['id']}"):

                    if not is_pro and build_count >= 3:

                        st.error("🚫 Free limit reached")

                        st.markdown("""
                        ### 🚀 Upgrade to Pro

                        Unlock:
                        - Unlimited startup builds
                        - Better AI quality
                        - Priority features

                        💰 Price: ₹299/month
                        """)

                        if st.button("💳 Pay Now", key=f"pay_{row['id']}"):

                            try:
                                res = requests.post(
                                    "https://payment-server-f778.onrender.com/create-order",
                                    json={"user_id": st.session_state.user}
                                )

                                data = res.json()

                                st.success("✅ Order Created!")
                                st.json(data)

                            except Exception as e:
                                st.error(f"Payment error: {e}")

                    else:
                        st.session_state.generated_plans[row["id"]] = generate_full_startup_plan(row["problem"])

                        increment_build_count(
                            st.session_state.user,
                            build_count,
                            st.session_state.token
                        )

                        st.rerun()

            # ---- SHOW PLAN (FIXED POSITION) ----
            if row["id"] in st.session_state.generated_plans:

                if not is_pro and build_count >= 3:
                    st.warning("🔒 Upgrade to view this startup plan")
                    continue

                import json, re

                plan_raw = st.session_state.generated_plans[row["id"]]

                match = re.search(r"\{.*\}", plan_raw, re.DOTALL)
                clean = match.group() if match else plan_raw

                clean = clean.replace("→", "->")
                clean = clean.replace("₹", "Rs")

                safe_clean = clean.encode("ascii", "ignore").decode()

                try:
                    parsed = json.loads(safe_clean)
                except:
                    parsed = None

                if parsed:
                    st.subheader(parsed.get("startup_name", "Startup"))
                    st.caption(parsed.get("tagline", ""))

                    st.write(parsed.get("problem_analysis", ""))
                    st.write(parsed.get("solution", ""))
                    st.write(parsed.get("target_users", ""))

                    for f in parsed.get("features", []):
                        st.write(f"• {f}")

                    st.write(parsed.get("revenue_plan", ""))

                else:
                    st.code(plan_raw)

    else:
        st.info("No problems found for this user")

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

    if page == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = sign_in(email, password)

            if "access_token" in result:
                user_id = result["user"]["id"]

                st.session_state.user = user_id
                st.session_state.token = result["access_token"]

                profile = get_profile(user_id, st.session_state.token)

                if not profile:
                    insert_profile(user_id, "User", "", st.session_state.token)
                    profile = get_profile(user_id, st.session_state.token)

                if profile:
                    st.session_state.name = f"{profile['first_name']} {profile['last_name']}"
                else:
                    st.session_state.name = "User"

                st.rerun()
            else:
                st.error("Invalid login")

    elif page == "Register":

        st.subheader("Create Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            result = sign_up(email, password)

            if "user" in result:
                st.success("Account created! Please login.")
            else:
                st.error("Registration failed")

    elif page == "Reset Password":
        email = st.text_input("Email")

        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Email sent")
