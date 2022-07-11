# from urllib import request
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import *
from .serializers import *
from .forms import *
from rest_framework import status, generics
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from safaris.api import permissions
from safaris.models import *
from rest_framework.response import Response
from safaris.api.serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from safaris.api.permissions import IsTouristUser, IsTourguideUser
from safaris.api.permissions import IsAdminOrReadOnly
from email import message
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .mpesa_credentials import *
from django.shortcuts import render, redirect
import time
from decouple import config
from rest_framework import viewsets
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.template.loader import render_to_string  
from .token import account_activation_token   
from django.core.mail import EmailMessage  

from drf_yasg.views import get_schema_view

User = get_user_model()
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

class SignUpViewSet(viewsets.ModelViewSet):  
      serializer_class = SignUpSerializer
      queryset = User.objects.all()

class UpdateUserProfileViewSet(viewsets.ModelViewSet):  
      serializer_class = UpdateUserProfileSerializer
      queryset = Profile.objects.all()

class TouristSignupView(generics.GenericAPIView):
    serializer_class = TouristSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        })
class TourguideSignupView(generics.GenericAPIView):
    serializer_class = TourguideSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_tourist': user.is_tourist,
            'is_tourguide': user.is_tourguide,
            
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

class TouristOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsTouristUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class TourguideOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsTourguideUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class TouristViewSet(viewsets.ModelViewSet):  
      serializer_class = TouristSerializer
      queryset = Tourist.objects.all()

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
        "AccountReference": "Virtual-Safaris",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')
    
class TourguideList(APIView):
    def get(self, request, format=None):
        all_projects = Tourguide.objects.all()
        serializers = TourguideSerializer(all_projects, many=True)
        return Response(serializers.data)

def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save() 
 # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, '', {'form': form}) 

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  

# @login_required(login_url='login')
# def profile(request, username):
#     return render(request, 'profile')
@login_required
def profile(request):

    if request.method == 'POST':
        form = UpdateUserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')
    else:
        form = UpdateUserProfileForm()

    return render(request, '', {'form':form})

def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, '', params)

@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form
         }
    return render(request, 'profile', params)

