from django import forms
from xml.etree.ElementInclude import include
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *  # NOQA

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name','profile_image','contact','email','bio','address']
       
class PaymentForm(forms.ModelForm):
    id = forms.IntegerField()
    name = forms.CharField()
    amount=forms.IntegerField(required=True)
    contact= forms.IntegerField(required=True)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TouristForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username',  'email', 'password']

    def save(self):
        user = super().save(commit=False)
        user.is_tourist = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        tourist = Tourist.objects.create(user=user)
        tourist.email = self.cleaned_data.get('email')
        tourist.save()

        return tourist
