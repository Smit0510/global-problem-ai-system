from flask import Flask, request, jsonify
import razorpay
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# ✅ Razorpay keys (Render ENV)
RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))


@app.route("/")
def home():
    return "Server is running"


@app.route("/create-order", methods=["POST"])
def create_order():
    try:
        data = request.get_json(force=True)
        user_id = data.get("user_id")

        order = client.order.create({
            "amount": 29900,  # ₹299
            "currency": "INR",
            "payment_capture": 1
        })

        return jsonify({
            "order_id": order["id"],
            "amount": order["amount"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ IMPORTANT (Render fix)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
