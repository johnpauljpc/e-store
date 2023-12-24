import math, random, requests
from django.conf import settings



def process_payment(order, ref):
    auth_token= settings.FLUTTERWAVE_SK
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
    "tx_ref":''+ref,
    "amount":order.order_total(),
    "currency":"NGN",
    "redirect_url": f"http://localhost:8000/confirm-payment/{ref}/",
    "payment_options":"card",
    "meta":{
    "consumer_id":order.user.id,
    "consumer_mac":"92a3-912ba-1192a"
    },
    "customer":{
    "email":order.user.email,
    "phonenumber":int(order.billing_address.phone_number),
    "name":str(order.user.first_name)
    },

    "customizations":{
    "title":"JPC Collection store",
    "description":"Best store in Nigeria",
    "logo":"https://avatars.githubusercontent.com/u/63419117?v=4"
    }
    }
    url = 'https://api.flutterwave.com/v3/payments'
    
    try:
        response = requests.post(url, json=data, headers=hed)
        response=response.json()
        link=response['data']['link']
        return link
    except Exception as err:
        print("Errroooo   ", err)
        return "http://localhost:8000/"