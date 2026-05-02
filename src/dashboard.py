import streamlit as st
import requests
import streamlit.components.v1 as components
import json, re, time

from supabase_auth import (
    sign_up, sign_in, reset_password,
    insert_problem, get_problems, delete_problem,
    upvote_problem,
    insert_profile, get_profile,
    get_build_data, increment_build_count
)

from ai_generator import generate_full_startup_plan

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="AI Startup Builder", layout="wide")


# ---------------- PDF ----------------
def generate_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Startup Plan", styles["Title"]))
    elements.append(Spacer(1, 12))

    for line in text.split("\n"):
        elements.append(Paragraph(line, styles["BodyText"]))
        elements.append(Spacer(1, 8))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# ---------------- SESSION ----------------
if "generated_plans" not in st.session_state:
    st.session_state.generated_plans = {}

if "user" not in st.session_state:
    st.session_state.user = None

if "token" not in st.session_state:
    st.session_state.token = None

if "name" not in st.session_state:
    st.session_state.name = "User"


# ---------------- DASHBOARD ----------------
def show_dashboard():

    top1, top2 = st.columns([4,1])

    with top1:
        st.title("🚀 AI Startup Builder")
        st.caption("Turn problems into validated startups")

    # 💎 PAYMENT BUTTON (FIXED)
    with top2:
        if st.button("💎 Upgrade to Pro"):

            try:
                # 🔥 Wake server (Render fix)
                requests.get("https://payment-server-f778.onrender.com/")
                time.sleep(1)

                res = requests.post(
                    "https://payment-server-f778.onrender.com/create-order",
                    json={"user_id": st.session_state.user},
                    timeout=10
                )

                if res.status_code != 200:
                    st.error(f"Server error: {res.status_code}")
                    st.text(res.text)
                    return

                try:
                    data = res.json()
                except:
                    st.error("❌ Invalid response from server")
                    st.text(res.text)
                    return

                order_id = data.get("order_id")

                if not order_id:
                    st.error("❌ Order ID missing")
                    st.json(data)
                    return

                st.success("✅ Order Created!")

                checkout = f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                <script>
                var options = {{
                    "key": "rzp_live_Sk3uDNJeDvuR3s",
                    "amount": "29900",
                    "currency": "INR",
                    "name": "AI Startup Builder",
                    "description": "Upgrade to Pro",
                    "order_id": "{order_id}",
                    "handler": function (response){{
                        fetch("https://payment-server-f778.onrender.com/verify-payment", {{
                            method: "POST",
                            headers: {{ "Content-Type": "application/json" }},
                            body: JSON.stringify({{
                                razorpay_payment_id: response.razorpay_payment_id,
                                razorpay_order_id: response.razorpay_order_id,
                                razorpay_signature: response.razorpay_signature,
                                user_id: "{st.session_state.user}"
                            }})
                        }})
                        .then(() => {{
                            alert("✅ PRO Activated!");
                            window.location.reload();
                        }})
                        .catch(() => {{
                            alert("Payment done but verification failed");
                        }});
                    }}
                }};
                new Razorpay(options).open();
                </script>
                """

                components.html(checkout, height=400)

            except Exception as e:
                st.error(f"Payment error: {e}")

    # USER DATA
    user_data = get_build_data(st.session_state.user, st.session_state.token)
    build_count = user_data.get("build_count", 0)
    is_pro = user_data.get("is_pro", False)

    if is_pro:
        st.success("🚀 PRO User — Unlimited Builds")
    else:
        st.info(f"🧠 Builds used: {build_count}/3")

    # ADD PROBLEM
    problem = st.text_input("Enter a real-world problem")

    if st.button("Add Problem"):
        if problem.strip():
            insert_problem(problem, "Other", "", st.session_state.token, st.session_state.user)
            st.rerun()

    # PROBLEMS LIST
    problems = get_problems(st.session_state.token, st.session_state.user) or []

    for row in problems:

        st.markdown(f"### 🚧 {row['problem']}")
        st.write(f"👍 {row.get('votes',0)} votes")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("👍", key=f"vote_{row['id']}"):
                upvote_problem(row["id"], row.get("votes", 0), st.session_state.token)
                st.rerun()

        with col2:
            if st.button("🗑 Delete", key=f"del_{row['id']}"):
                delete_problem(row["id"], st.session_state.token)
                st.rerun()

        with col3:
            if st.button("🚀 Build", key=f"build_{row['id']}"):

                if not is_pro and build_count >= 3:
                    st.warning("Upgrade to continue")
                else:
                    plan = generate_full_startup_plan(row["problem"])
                    st.session_state.generated_plans[row["id"]] = plan

                    increment_build_count(
                        st.session_state.user,
                        build_count,
                        st.session_state.token
                    )
                    st.rerun()

        # SHOW PLAN
        if row["id"] in st.session_state.generated_plans:

            raw = st.session_state.generated_plans[row["id"]]

            match = re.search(r"\{.*\}", raw, re.DOTALL)
            clean = match.group() if match else raw

            try:
                data = json.loads(clean)
            except:
                data = None

            if data:

                st.markdown(f"#### 🔥 Score: {data.get('startup_score','N/A')} / 10")

                tags = data.get("validation_tags", [])
                if tags:
                    st.write(" ".join([f"🏷️ {t}" for t in tags]))

                st.write(f"📊 Market: {data.get('market_size')}")
                st.write(f"📈 Demand: {data.get('demand_level')}")
                st.write(f"⚔️ Competition: {data.get('competition_level')}")

                st.subheader("Solution")
                st.write(data.get("solution"))

                st.subheader("Features")
                for f in data.get("features", []):
                    st.write(f"• {f}")

                pdf = generate_pdf(raw)

                st.download_button(
                    "📄 Export PDF",
                    pdf,
                    file_name=f"{data.get('startup_name','startup')}.pdf",
                    key=f"pdf_{row['id']}"
                )

            else:
                st.code(raw)

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()


# ---------------- AUTH ----------------
if st.session_state.user:
    show_dashboard()

else:

    page = st.radio("Select", ["Login", "Register"], horizontal=True)

    # LOGIN
    if page == "Login":

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login"):
                result = sign_in(email, password)

                if "access_token" in result:
                    user_id = result["user"]["id"]

                    st.session_state.user = user_id
                    st.session_state.token = result["access_token"]

                    profile = get_profile(user_id, st.session_state.token)

                    if profile:
                        st.session_state.name = f"{profile['first_name']} {profile['last_name']}"

                    st.rerun()
                else:
                    st.error("Invalid login")

        with col2:
            if st.button("Forgot Password"):
                if email:
                    reset_password(email)
                    st.success("Reset email sent")
                else:
                    st.error("Enter email first")

    # REGISTER
    else:

        st.subheader("Create Account")

        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):

            result = sign_up(email, password)

            if "user" in result:

                user_id = result["user"]["id"]

                insert_profile(
                    user_id,
                    first_name,
                    last_name,
                    result.get("access_token")
                )

                st.success("Account created! Please login.")

            else:
                st.error("Registration failed")
