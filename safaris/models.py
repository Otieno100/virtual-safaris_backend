from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from virtualSafaris.settings import AUTH_USER_MODEL
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    is_tourist = models.BooleanField(default=False)
    is_tourguide = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def save_user(self):
        self.save()

    def update_user(self):
        self.update()

    def delete_user(self):
        self.delete()


#   def __str__(self):
#         return self.username


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Safaris(models.Model):
   
    name = models.CharField(max_length=344)
    description = models.TextField()
    location = models.CharField(max_length=400)
    pub_date = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('safais-image', null=True)
    video = CloudinaryField('safaris-video', null=True, default=None)
    
    

    def __str__(self):
        return self.name


class Payment(models.Model):
    amount = models.PositiveIntegerField(default=100)
    contact = models.PositiveIntegerField(
        null=False, blank=False, unique=True, default=254799735661)

    def __str__(self):
        return f'{self.name} payment'

    def save_payment(self):
        self.save()


class Tourguide(models.Model):

    user = models.OneToOneField(
        User, related_name='tourguide', on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=255, default='')
    contact = models.PositiveIntegerField(
        null=False, blank=False, unique=True, default=254799735661)
    location = models.IntegerField(blank=True, default='')
    address = models.CharField(max_length=255, default='')
    company_bio = models.CharField(max_length=255, default='')
    company_pic = CloudinaryField(
        'image', default='https://res.cloudinary.com/albrighthuman/image/upload/v1654439561/cld-sample-2.jpg')
   


    def save_tourguide(self):
        self.save()

    def delete_tourguide(self):
        self.delete()

    @classmethod
    def search_by_company_name(cls, search_term):
        company = cls.objects.filter(title__icontains=search_term)
        return company

    def __str__(self):
        return self.name


class Profile(models.Model):

    id = models.IntegerField(User, primary_key=True)
    full_name = models.CharField(max_length=255, default='')
    contact = models.PositiveIntegerField(
        null=False, blank=False, unique=True, default=254799735661)
    email = models.CharField(max_length=255, default='')
    bio = models.CharField(max_length=255, default='')
    profile_image = CloudinaryField(
        'image', default='https://res.cloudinary.com/albrighthuman/image/upload/v1654536946/hjiaxew1u4pydlw3wljo.jpg')
    bio = models.TextField(max_length=500, default='', blank=True)
    address = models.CharField(max_length=100, default='')


class Tourist(models.Model):
    user = models.OneToOneField(
        User, related_name='tourist', on_delete=models.CASCADE, default='')
    profile_photo = CloudinaryField(
        'image',  blank=True, default='https://res.cloudinary.com/albrighthuman/image/upload/v1654536946/hjiaxew1u4pydlw3wljo.jpg')
    bio = models.TextField(blank=True, default='')
    location = models.CharField(max_length=100,  blank=True, default='')
    contact = models.PositiveIntegerField(
        null=False, blank=False, unique=True, default=254799735661)
    name = models.IntegerField(blank=False, default='')
    email = models.CharField(max_length=50, blank=True, default='')
    password = models.CharField(max_length=50, blank=False, default='')
   

    def __str__(self):
        return self.name

    def save_tourist(self):
        self.save()

    def delete_tourist(self):
        self.delete()

    @classmethod
    def update_tourist(self):
        self.update()
