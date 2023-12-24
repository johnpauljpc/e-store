import requests
from django.conf import settings
from django.http import HttpResponseRedirect

SECRET_KEY = settings.PAYSTACK_SK
paystack_url = 'https://api.paystack.co/transaction/initialize'
def process_payment(order, ref):
    headers = {
        'Authorization': f'Bearer {SECRET_KEY}',  # Replace with your Paystack secret key
        'Content-Type': 'application/json',
    }
    data = {
        'email':order.user.email,
        'amount': order.order_total() * 100,  # Amount should be in kobo (lowest currency unit)
        'reference': ref,
        "send_otp":True,
        "phonenumber":int(order.billing_address.phone_number),
        "name":str(order.user.first_name),
        'callback_url': f"http://localhost:8000/confirm-payment/{ref}/",  # Set your callback URL
        "metadata": {
            "cancel_action": "http://localhost:8000/cancel-payment/"
            },
    }


    response = requests.post(paystack_url, headers=headers, json=data)
    payment_data = response.json()
    print(payment_data)
    link = (payment_data['data']['authorization_url'])
    return link