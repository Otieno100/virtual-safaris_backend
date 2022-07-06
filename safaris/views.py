from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Safaris
from .serializer import SafarisSerializer
from rest_framework import status


import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

# Create your views here.


class HelloKenya(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {
            'message':"HelloKenya"
        }
        return Response(content)
    
class Extractor(APIView):
    parser_classes = (IsAuthenticated,)
    def get(self, request):
        content = {
                'username':request.user.username,
                'password': request.user.password,
            }
        return Response(content)



class safaris(APIView):
    def get(self, request, format=None):
        safaris = Safaris.objects.all()
        serializers = SafarisSerializer(safaris, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = SafarisSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    


# Create your views here.
def getAccessToken(request):
    consumer_key='aOBujkcJv34nJ9qfX7xSXk6LrDqjAJmi'
    consumer_secret='8WxEPd0jKrrGoIao'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)



def lipa_na_mpesa_online(request, phonenumber, amount):
    phonenumber_int = int(phonenumber)
    amount_int = int(amount)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount_int,
        "PartyA": phonenumber_int,  
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phonenumber_int, 
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Albright.Human",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')
