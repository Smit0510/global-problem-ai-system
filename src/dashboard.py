import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# ---------------------------
# Page configuration
# ---------------------------

st.set_page_config(
    page_title="AI Problem Discovery Dashboard",
    layout="wide"
)

st.title("🚀 AI Problem Discovery Dashboard")

# ---------------------------
# Load config file
# ---------------------------

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# ---------------------------
# Initialize authenticator
# ---------------------------

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# ---------------------------
# LOGIN
# ---------------------------

authenticator.login("main")

authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")

# ---------------------------
# REGISTER USER
# ---------------------------

if authentication_status is None:

    st.subheader("Register New Account")

    try:
        if authenticator.register_user("main"):
            st.success("User registered successfully")
    except Exception as e:
        st.error(e)

# ---------------------------
# FORGOT PASSWORD
# ---------------------------

if authentication_status is None:

    st.subheader("Forgot Password")

    try:
        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password("main")

        if username_forgot_pw:
            st.success("New password generated successfully")
            st.write("Username:", username_forgot_pw)
            st.write("New Password:", random_password)

        elif username_forgot_pw == False:
            st.error("Username not found")

    except Exception as e:
        st.error(e)

# ---------------------------
# LOGIN STATUS
# ---------------------------

if authentication_status == False:
    st.error("Username/password incorrect")

elif authentication_status:

    authenticator.logout("Logout", "sidebar")

    st.sidebar.write(f"Welcome **{name}**")

    st.success("Logged in successfully")

    st.header("Dashboard")

    st.write("This is your AI Problem Discovery Dashboard.")

    st.write("Next we will add AI features and monetization.")
