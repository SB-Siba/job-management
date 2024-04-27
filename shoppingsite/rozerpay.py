import razorpay
from django.conf import settings
 
def create_order_in_razPay(amount,receipt="order_rcptid_12"):
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        print(client)
        data = {
            "amount": amount,
            "currency": "INR",
            "receipt": receipt,
            "partial_payment":False,
        }
        print(data)
        order = client.order.create(data=data)
        print("Order created successfully:", order)
        return (True, order['id'])
 
    except Exception as e:
        print(e)
        return (False, str(e))
 
def verify_signature(response_data):
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    return client.utility.verify_payment_signature(response_data)