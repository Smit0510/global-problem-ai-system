import razorpay
import os

client = razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))

def create_order(amount):
    order = client.order.create({
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": 1
    })
    return order
