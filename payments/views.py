from django.shortcuts import render
from django.http import JsonResponse
import requests
import json

# Replace with your actual credentials
CONSUMER_KEY = 'ZzI0lrQfBlcKXPZsRJhvckrdCpEqtWZiIighOKN31AaWZjSI'
CONSUMER_SECRET = 'kJdg5Z6NqQTx3suZe808w19XeuE8Db3zcixvyhYqlRlODnGoGYat259cldIOBiFB'
SHORTCODE = '174379'  # Sandbox shortcode
PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0d72a1d11c00c55e368d2b19da7d1b'
CALLBACK_URL = 'http://127.0.0.1:8080/payments/initialize_payment/'

# Create your views here.

def initialize_payment1(request):
    if request.method == "POST":
        # Initialize payment here
        phone = request.POST.get('phoneNumber')
        amount = request.POST.get('amount')
        print("phone", phone)
        return JsonResponse({"message": "Payment initialized successfully"})
    return render(request, "initialize_payment.html")

def generate_password():
    # Generate password (BusinessShortCode + Passkey + Timestamp)
    timestamp = generate_timestamp()
    return f"{SHORTCODE}{PASSKEY}{timestamp}"

def generate_timestamp():
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d%H%M%S')

def callback(request):
    if request.method == 'POST':
        response_data = json.loads(request.body)
        # Handle the response data as needed (e.g., log it, update transaction status)
        return JsonResponse({'message': 'Callback received.'}, status=200)




def initialize_payment(request):
    if request.method == 'POST':
        import requests

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer P1Zjro2IlFdC0Wlj1spECfl7Di54'
        }
        payload = {
            "BusinessShortCode": 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQxMjA5MDY1NzE4",
            "Timestamp": "20241209065718",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": 254716260730,
            "PartyB": 174379,
            "PhoneNumber": 254716260730,
            "CallBackURL": "https://192.168.2.172:8000/callback",
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X" 
        }

        response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
        print(response.text.encode('utf8'))
        # *** Authorization Request in Python ***|
 
        # url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        # querystring = {"grant_type":"client_credentials"}
        # payload = ""
        # headers = {
        #     "Authorization": "Basic SWZPREdqdkdYM0FjWkFTcTdSa1RWZ2FTSklNY001RGQ6WUp4ZVcxMTZaV0dGNFIzaA=="
        # }
        # response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        # print(response.text)
        # return JsonResponse({"message": "Payment initialized successfully"})
        # phone_number = request.POST.get('phoneNumber')
        # amount = request.POST.get('amount')

        # print(phone_number,amount)

        # if not phone_number or not amount:
        #     return JsonResponse({'error': 'Phone number and amount are required.'}, status=400)

        # access_token = generate_access_token()
        # url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        # headers = {
        #     'Authorization': f'Bearer {access_token}',
        #     'Content-Type': 'application/json',
        # }

        # payload = {
        #     "BusinessShortCode": SHORTCODE,
        #     "Password": generate_password(),
        #     "Timestamp": generate_timestamp(),
        #     "TransactionType": "CustomerPayBillOnline",
        #     "Amount": amount,
        #     "PartyA": phone_number,
        #     "PartyB": SHORTCODE,
        #     "PhoneNumber": phone_number,
        #     "CallBackURL": CALLBACK_URL,
        #     "AccountReference": "HotelPayment",
        #     "TransactionDesc": "Payment for hotel booking"
        # }

        # response = requests.post(url, headers=headers, data=json.dumps(payload))
        # return JsonResponse(response.json(), status=response.status_code)

    return render(request, 'initialize_payment.html')

def callback(request):
    if request.method == 'POST':
        response_data = json.loads(request.body)
        # Handle the response data as needed (e.g., log it, update transaction status)
        return JsonResponse({'message': 'Callback received.'}, status=200)