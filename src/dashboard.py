import streamlit as st
from supabase_auth import sign_up, sign_in, reset_password, insert_problem, get_problems

st.set_page_config(page_title="AI Problem Dashboard")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "token" not in st.session_state:
    st.session_state.token = None


# ---------------- DASHBOARD ----------------
def show_dashboard():
    st.title("🚀 AI Problem Discovery Dashboard")
    st.success(f"Logged in as {st.session_state.user}")

    # ---- ADD PROBLEM ----
    st.subheader("➕ Add Problem")

    problem = st.text_input("Enter a problem")

    if st.button("Save Problem"):
        if problem:
            insert_problem(
                problem,
                st.session_state.token,
                st.session_state.user
            )
            st.success("Problem saved!")
        else:
            st.warning("Please enter a problem")

    # ---- SHOW PROBLEMS ----
    st.subheader("📋 Your Problems")

    data = get_problems(st.session_state.token)

    if isinstance(data, list) and len(data) > 0:
        for row in data:
            st.write(f"• {row['problem']}")
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
