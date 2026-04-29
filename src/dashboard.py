import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(page_title="AI Problem Discovery Dashboard", layout="wide")

# -------------------------
# LOAD CONFIG
# -------------------------

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# -------------------------
# SESSION STATE PAGE CONTROL
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "login"

# -------------------------
# LOGIN PAGE
# -------------------------

if st.session_state.page == "login":

    st.title("🔐 Login")

    authenticator.login("main")

    authentication_status = st.session_state.get("authentication_status")
    name = st.session_state.get("name")

    if authentication_status == False:
        st.error("Username/password incorrect")

    if authentication_status:
        st.session_state.page = "dashboard"
        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create Account"):
            st.session_state.page = "register"
            st.rerun()

    with col2:
        if st.button("Forgot Password"):
            st.session_state.page = "forgot"
            st.rerun()

# -------------------------
# REGISTER PAGE
# -------------------------

elif st.session_state.page == "register":

    st.title("📝 Register")

    try:
        register_status = authenticator.register_user("main")

        if register_status:
            st.success("User registered successfully. You can now login.")

    except Exception as e:
        st.error(e)

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# -------------------------
# FORGOT PASSWORD PAGE
# -------------------------

elif st.session_state.page == "forgot":

    st.title("🔑 Reset Password")

    try:
        username_forgot_pw, email_forgot_pw, new_password = authenticator.forgot_password("main")

        if username_forgot_pw:
            st.success("New password generated")

            st.write("Username:", username_forgot_pw)
            st.write("New Password:", new_password)

        elif username_forgot_pw == False:
            st.error("Username not found")

    except Exception as e:
        st.error(e)

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# -------------------------
# DASHBOARD PAGE
# -------------------------

elif st.session_state.page == "dashboard":

    st.title("🚀 AI Problem Discovery Dashboard")

    authenticator.logout("Logout", "sidebar")

    name = st.session_state.get("name")

    st.sidebar.write(f"Welcome **{name}**")

    st.success("Login successful")

    st.write("Your dashboard will appear here.")

    st.write("Next we will add AI features and monetization.")
