import os
import razorpay
from flask import Flask, request, jsonify

app = Flask(__name__)

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


# ✅ CREATE ORDER API
@app.route("/create-order", methods=["POST"])
def create_order():

    data = request.json
    user_id = data.get("user_id")

    order = client.order.create({
        "amount": 29900,  # ₹299
        "currency": "INR",
        "payment_capture": 1,
        "notes": {
            "user_id": user_id
        }
    })

    return jsonify(order)


if __name__ == "__main__":
    if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
