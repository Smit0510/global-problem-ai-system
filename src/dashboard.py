import streamlit as st
import requests
import streamlit.components.v1 as components

from supabase_auth import (
    sign_up, sign_in,
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
def generate_pdf(plan_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("AI Startup Plan", styles["Title"]))
    elements.append(Spacer(1, 12))

    for line in plan_text.split("\n"):
        if line.strip():
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

    # 🔥 HEADER WITH RIGHT BUTTON
    col1, col2 = st.columns([4, 1])

    with col1:
        st.title("🚀 AI Startup Builder")
        st.success(f"Welcome {st.session_state.name} 👋")

    with col2:
        if st.button("🚀 Upgrade to Pro"):
            try:
                res = requests.post(
                    "https://payment-server-f778.onrender.com/create-order",
                    json={"user_id": st.session_state.user},
                    timeout=10
                )

                data = res.json()
                order_id = data.get("order_id")

                if order_id:
                    checkout_html = f"""
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
                                headers: {{
                                    "Content-Type": "application/json"
                                }},
                                body: JSON.stringify({{
                                    razorpay_payment_id: response.razorpay_payment_id,
                                    razorpay_order_id: response.razorpay_order_id,
                                    razorpay_signature: response.razorpay_signature,
                                    user_id: "{st.session_state.user}"
                                }})
                            }})
                            .then(res => res.json())
                            .then(data => {{
                                alert("✅ Payment Successful & PRO Activated!");
                                window.location.reload();
                            }});
                        }}
                    }};
                    var rzp = new Razorpay(options);
                    rzp.open();
                    </script>
                    """

                    components.html(checkout_html, height=500)

            except Exception as e:
                st.error(f"Payment error: {e}")

    # ---------------- USER DATA ----------------
    user_data = get_build_data(st.session_state.user, st.session_state.token)
    build_count = user_data.get("build_count", 0)
    is_pro = user_data.get("is_pro", False)

    # ✅ CLEAN STATUS
    if is_pro:
        st.success("🚀 PRO User — Unlimited Builds")
    else:
        st.info(f"🧠 Builds used: {build_count}/3")

    # ---------------- ADD PROBLEM ----------------
    problem = st.text_input("Enter problem")

    if st.button("Save Problem"):
        insert_problem(problem, "Other", "", st.session_state.token, st.session_state.user)
        st.rerun()

    # ---------------- LIST ----------------
    data = get_problems(st.session_state.token, st.session_state.user)

    if isinstance(data, list):

        for row in data:

            st.markdown(f"### 🚧 {row['problem']}")
            st.write(f"👍 {row.get('votes', 0)} votes")

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

                    if not is_pro and build_count >= 3:
                        st.error("🚫 Free limit reached")
                    else:
                        st.session_state.generated_plans[row["id"]] = generate_full_startup_plan(row["problem"])

                        increment_build_count(
                            st.session_state.user,
                            build_count,
                            st.session_state.token
                        )
                        st.rerun()

            # -------- PLAN + PDF --------
            if row["id"] in st.session_state.generated_plans:

                if not is_pro and build_count >= 3:
                    st.warning("🔒 Upgrade to view this plan")
                    continue

                plan = st.session_state.generated_plans[row["id"]]

                st.subheader("🚀 Generated Startup Plan")
                st.write(plan)

                pdf = generate_pdf(plan)

                st.download_button(
                    "📄 Download PDF",
                    pdf,
                    file_name="startup_plan.pdf",
                    mime="application/pdf"
                )

    # LOGOUT
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()


# ---------------- AUTH ----------------
if st.session_state.user:
    show_dashboard()

else:
    page = st.radio("Select Page", ["Login", "Register"], horizontal=True)

    if page == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = sign_in(email, password)

            if "access_token" in result:
                st.session_state.user = result["user"]["id"]
                st.session_state.token = result["access_token"]
                st.rerun()
            else:
                st.error("Invalid login")

    elif page == "Register":

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            result = sign_up(email, password)

            if "user" in result:
                st.success("Account created! Login now")
            else:
                st.error("Registration failed")
