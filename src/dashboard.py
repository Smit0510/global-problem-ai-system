import streamlit as st
from supabase_auth import (
    sign_up,
    sign_in,
    reset_password,
    insert_problem,
    get_problems,
    delete_problem,
    upvote_problem   # ✅ ADD THIS
)
from ai_generator import generate_problems

# ✅ MUST BE FIRST
st.set_page_config(page_title="AI Problem Dashboard")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "token" not in st.session_state:
    st.session_state.token = None

if "problem_input" not in st.session_state:
    st.session_state.problem_input = ""

# ---------------- DASHBOARD ----------------
def show_dashboard():
    st.title("🚀 AI Problem Discovery")
    st.caption("Find real-world problems & build startups")

    st.success(f"Logged in as {st.session_state.user}")

    # ---- ADD PROBLEM ----
    st.subheader("➕ Add Problem")

    problem = st.text_input(
        "Enter a real-world problem",
        value=st.session_state.problem_input
    )

    # 🔥 SMART CATEGORY AUTO-DETECT
    categories = ["Education", "Finance", "Health", "Productivity", "Startup", "Other"]

    default_category = "Other"

    if problem:
        p = problem.lower()
        if "student" in p or "study" in p:
            default_category = "Education"
        elif "money" in p or "bill" in p:
            default_category = "Finance"
        elif "health" in p or "gym" in p:
            default_category = "Health"
        elif "focus" in p or "productivity" in p:
            default_category = "Productivity"
        elif "startup" in p:
            default_category = "Startup"

    category = st.selectbox(
        "Select Category",
        categories,
        index=categories.index(default_category)
    )

    tags = st.text_input(
        "Tags (comma separated)",
        placeholder="e.g. students, money, fitness"
    )

    if st.button("Save Problem"):

        if problem and len(problem.strip()) > 5:

            result = insert_problem(
                problem.strip(),
                category,
                tags,
                st.session_state.token,
                st.session_state.user
            )

            if isinstance(result, dict) and "error" in result:
                st.error(f"Error: {result}")
            else:
                st.success("Problem saved!")
                st.session_state.problem_input = ""
                st.rerun()

        else:
            st.warning("Enter a meaningful problem (min 5 characters)")

    # ---- AI SUGGESTIONS ----
    st.subheader("💡 AI Suggestions")

    if st.button("Generate Ideas"):
        suggestions = generate_problems(problem if problem else "startup problems")

        for idea in suggestions:
            st.markdown(f"💡 {idea}")

    # ---- SEARCH + FILTER ----
    st.subheader("🔍 Search & Filter")

    search_query = st.text_input("Search problems")

    filter_category = st.selectbox(
        "Filter by Category",
        ["All"] + categories
    )

    # ---- SHOW PROBLEMS ----
    st.subheader("📋 Your Problems")

    data = get_problems(st.session_state.token)

    if isinstance(data, list) and len(data) > 0:

        # 🔥 APPLY FILTERS
        filtered_data = []

        for row in data:
            text = row.get("problem", "").lower()
            cat = (row.get("category") or "").lower()

            # search match
            if search_query and search_query.lower() not in text:
                continue

            # category filter
            if filter_category != "All" and cat != filter_category.lower():
                continue

            filtered_data.append(row)

        if len(filtered_data) == 0:
            st.info("No matching problems found")
            return

        for row in filtered_data:
            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(f"""
                <div style="padding:10px; border-radius:10px; background:#1e1e1e; margin-bottom:10px">
                    🚧 {row['problem']}<br><br>
                    <b>📂 Category:</b> {row.get('category','-')}<br>
                    <b>🏷️ Tags:</b> {row.get('tags','-')}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button("❌", key=row["id"]):
                    delete_problem(row["id"], st.session_state.token)
                    st.rerun()

    else:
        st.info("No problems yet")

    # ---- LOGOUT ----
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

    # ---------- LOGIN ----------
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

    # ---------- REGISTER ----------
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

    # ---------- RESET PASSWORD ----------
    elif page == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input("Email", key="reset_email")

        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Password reset email sent")
