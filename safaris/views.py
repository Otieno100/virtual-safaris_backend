from urllib import request
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Safaris, Tourguide
from .serializer import SafarisSerializer, TourguideSerializer
from rest_framework import status


import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

# ali
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
# api 


from .models import  Profile
from .serializers import ProfileSerializer


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
    
class TourguideList(APIView):
    def get(self, request, format=None):
        all_projects = Tourguide.objects.all()
        serializers = TourguideSerializer(all_projects, many=True)
        return Response(serializers.data)


#........
class ProfileList(APIView):
    def get(self, request, format=None):
        all_merch = Profile.objects.all()
        serializers =ProfileSerializer(all_merch, many=True)
        return Response(serializers.data)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})




def home(request):
    return render(request, 'home.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)
