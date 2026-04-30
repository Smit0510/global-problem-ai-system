import streamlit as st
from supabase_auth import (
    sign_up,
    sign_in,
    reset_password,
    insert_problem,
    get_problems,
    delete_problem,
    upvote_problem,
    get_trending_problems,
    update_ai_score
)
from ai_generator import generate_problems, generate_startup_kit
from ai_scorer import score_problem

# ✅ MUST BE FIRST
st.set_page_config(page_title="AI Problem Dashboard", layout="wide")

# 🎨 GLOBAL CSS
st.markdown("""
<style>
.stApp { background-color: #0e1117; }

.card {
    padding: 16px;
    border-radius: 14px;
    background: #1c1f26;
    margin-bottom: 12px;
    border: 1px solid #2a2d34;
}

.card-highlight {
    padding: 16px;
    border-radius: 14px;
    background: linear-gradient(145deg, #1a2a1f, #1f3a28);
    margin-bottom: 12px;
    border: 1px solid #2e5f3e;
}

.title { font-size: 17px; font-weight: 600; color: #fff; }
.meta { font-size: 13px; color: #aaa; }

input { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

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

    # 🧠 Rank
    def calculate_rank(row):
        return (row.get("ai_score", 0) or 0) * 2 + (row.get("votes", 0) or 0)

    # ---------------- ADD ----------------
    st.subheader("➕ Add Problem")

    problem = st.text_input("Enter a real-world problem", value=st.session_state.problem_input)

    categories = ["Education", "Finance", "Health", "Productivity", "Startup", "Other"]
    category = st.selectbox("Category", categories)
    tags = st.text_input("Tags (comma separated)")

    if st.button("Save Problem"):
        if problem and len(problem.strip()) > 5:
            insert_problem(problem, category, tags, st.session_state.token, st.session_state.user)
            st.session_state.problem_input = ""
            st.success("Saved!")
            st.rerun()

    # ---------------- AI ----------------
    st.subheader("💡 AI Suggestions")

    if st.button("Generate Ideas"):
        ideas = generate_problems(problem if problem else "startup problems")
        for i in ideas:
            st.markdown(f"💡 {i}")

    # ---------------- SEARCH ----------------
    search = st.text_input("🔍 Search problems")

    # ---------------- DATA ----------------
    data = get_problems(st.session_state.token)

    # ---------------- TABS ----------------
    tab1, tab2, tab3 = st.tabs(["📋 All", "🔥 Trending", "🏆 Best"])

    # ---------------- TAB 1 ----------------
    with tab1:

        if data:
            filtered = []

            for row in data:
                if search and search.lower() not in row["problem"].lower():
                    continue
                filtered.append(row)

            filtered = sorted(filtered, key=calculate_rank, reverse=True)

            for row in filtered:

                # 🔥 AUTO AI SCORING
                if row.get("ai_score") is None:
                    score = score_problem(row["problem"])
                    if score:
                        update_ai_score(row["id"], score, st.session_state.token)
                        st.rerun()

                st.markdown(f"""
                <div class="card">
                    <div class="title">🚧 {row['problem']}</div><br>

                    <div class="meta">
                        📂 {row.get('category','-')}<br>
                        🏷️ {row.get('tags','-')}<br><br>

                        👍 {row.get('votes',0)} |
                        🤖 {row.get('ai_score',0)}/10 |
                        ⭐ {calculate_rank(row)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ACTIONS
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
                    if st.button("🚀 Build Startup", key=f"kit_{row['id']}"):
                        kit = generate_startup_kit(row["problem"])
                        st.info(kit)

        else:
            st.info("No problems yet")

    # ---------------- TAB 2 ----------------
    with tab2:

        trending = get_trending_problems(st.session_state.token)

        if trending:
            for row in trending[:5]:
                st.markdown(f"""
                <div class="card">
                    <div class="title">🔥 {row['problem']}</div>
                    <div class="meta">👍 {row.get('votes',0)}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No trending data")

    # ---------------- TAB 3 ----------------
    with tab3:

        if data:
            ranked = sorted(data, key=calculate_rank, reverse=True)

            for row in ranked[:5]:
                st.markdown(f"""
                <div class="card-highlight">
                    <div class="title">🚀 {row['problem']}</div>
                    <div class="meta">
                        🤖 {row.get('ai_score',0)} |
                        👍 {row.get('votes',0)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data yet")

    # ---------------- LOGOUT ----------------
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
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
            res = sign_in(email, password)
            if "access_token" in res:
                st.session_state.user = email
                st.session_state.token = res["access_token"]
                st.rerun()

    elif page == "Register":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            res = sign_up(email, password)
            if "access_token" in res:
                st.session_state.user = email
                st.session_state.token = res["access_token"]
                st.rerun()

    elif page == "Reset Password":
        email = st.text_input("Email")
        if st.button("Send Reset Email"):
            reset_password(email)
            st.success("Email sent")
