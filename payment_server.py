from flask import Flask, request, jsonify
import razorpay
import os
import requests

app = Flask(__name__)

# Razorpay keys
RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))


@app.route("/")
def home():
    return "Server is running"


# ✅ CREATE ORDER
@app.route("/create-order", methods=["POST"])
def create_order():
    try:
        order = client.order.create({
            "amount": 100,
            "currency": "INR",
            "payment_capture": 1
        })

        return jsonify({
            "order_id": order["id"],
            "amount": order["amount"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ VERIFY PAYMENT
@app.route("/verify-payment", methods=["POST"])
def verify_payment():
    try:
        data = request.json

        payment_id = data.get("razorpay_payment_id")
        order_id = data.get("razorpay_order_id")
        signature = data.get("razorpay_signature")
        user_id = data.get("user_id")

        # 🔐 Verify signature
        params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }

        client.utility.verify_payment_signature(params_dict)

        # ✅ Update Supabase (make user PRO)
        res = requests.patch(
            f"{SUPABASE_URL}/rest/v1/profiles?id=eq.{user_id}",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json={"is_pro": True}
        )

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
