import streamlit as st
import requests
import streamlit.components.v1 as components
import json, re

from supabase_auth import (
    sign_up, sign_in,
    insert_problem, get_problems, delete_problem,
    upvote_problem,
    get_build_data, increment_build_count
)

from ai_generator import generate_full_startup_plan

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="AI Startup Builder", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.hero {
    padding: 25px;
    border-radius: 14px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
}

.metric {
    background: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PDF ----------------
def generate_pdf(plan_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Startup Plan", styles["Title"]))
    elements.append(Spacer(1, 12))

    for line in plan_text.split("\n"):
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


# ---------------- DASHBOARD ----------------
def show_dashboard():

    # HEADER
    col1, col2 = st.columns([4,1])

    with col1:
        st.markdown("""
        <div class="hero">
            <h2>🚀 AI Startup Builder</h2>
            <p>Turn problems into validated startups</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("💎 Upgrade to Pro"):

            try:
                res = requests.post(
                    "https://payment-server-f778.onrender.com/create-order",
                    json={"user_id": st.session_state.user}
                )

                data = res.json()
                order_id = data.get("order_id")

                if not order_id:
                    st.error("Order creation failed")
                    return

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
                            alert("✅ PRO Activated!");
                            window.location.reload();
                        }})
                        .catch(() => {{
                            alert("Payment success but verification failed");
                        }});
                    }}
                }};
                new Razorpay(options).open();
                </script>
                """

                components.html(checkout, height=500)

            except Exception as e:
                st.error(e)

    # USER DATA
    user_data = get_build_data(st.session_state.user, st.session_state.token)
    build_count = user_data.get("build_count", 0)
    is_pro = user_data.get("is_pro", False)

    problems = get_problems(st.session_state.token, st.session_state.user) or []

    # METRICS
    c1, c2, c3 = st.columns(3)

    c1.markdown(f'<div class="metric">Problems<br><b>{len(problems)}</b></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric">Builds<br><b>{build_count}</b></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric">Plan<br><b>{"PRO" if is_pro else "FREE"}</b></div>', unsafe_allow_html=True)

    st.divider()

    # ADD PROBLEM
    problem = st.text_input("Enter a real-world problem")

    if st.button("Add Problem"):
        if problem.strip():
            insert_problem(problem, "Other", "", st.session_state.token, st.session_state.user)
            st.rerun()

    # LIST
    if not problems:
        st.info("No problems yet. Add one to begin.")
        return

    for row in problems:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader(f"🚧 {row['problem']}")
        st.write(f"👍 {row.get('votes', 0)} votes")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("👍", key=f"v{row['id']}"):
                upvote_problem(row["id"], row.get("votes", 0), st.session_state.token)
                st.rerun()

        with col2:
            if st.button("🗑", key=f"d{row['id']}"):
                delete_problem(row["id"], st.session_state.token)
                st.rerun()

        with col3:
            if st.button("🚀 Build", key=f"b{row['id']}"):

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

            if not is_pro and build_count >= 3:
                st.warning("🔒 Upgrade to view this plan")
            else:

                raw = st.session_state.generated_plans[row["id"]]

                match = re.search(r"\{.*\}", raw, re.DOTALL)
                clean = match.group() if match else raw

                try:
                    data = json.loads(clean)
                except:
                    data = None

                if data:

                    st.markdown(f"### 🔥 Startup Score: {data.get('startup_score', 'N/A')} / 10")
                    st.caption(data.get("tagline", ""))

                    tags = data.get("validation_tags", [])
                    if tags:
                        st.write(" ".join([f"🏷️ {t}" for t in tags]))

                    st.divider()

                    st.write(f"📊 Market: {data.get('market_size')}")
                    st.write(f"📈 Demand: {data.get('demand_level')}")
                    st.write(f"⚔️ Competition: {data.get('competition_level')}")
                    st.write(f"💰 Monetization: {data.get('monetization')}")

                    st.subheader("Solution")
                    st.write(data.get("solution"))

                    st.subheader("Features")
                    for f in data.get("features", []):
                        st.write(f"• {f}")

                    pdf = generate_pdf(raw)

                    st.download_button(
                        "📄 Download PDF",
                        pdf,
                        file_name="startup_plan.pdf"
                    )

                else:
                    st.code(raw)

        st.markdown('</div>', unsafe_allow_html=True)

    # LOGOUT
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()


# ---------------- AUTH ----------------
if st.session_state.user:
    show_dashboard()

else:
    page = st.radio("Select", ["Login", "Register"], horizontal=True)

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

    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            result = sign_up(email, password)

            if "user" in result:
                st.success("Account created")
            else:
                st.error("Error")
