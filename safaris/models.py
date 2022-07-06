from django.db import models

from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Create your models here.

class Safaris(models.Model):
    """
    A class thaat determines how photos will be saved into the database
    """
    name = models.CharField(max_length=344)
    description = models.TextField()
    location = models.CharField(max_length=400)
    pub_date = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('safais-image', null=True)
    video = models.FileField(upload_to ="video/%y")
    

    def __str__(self):
      return self.name



class Payment(models.Model):
    amount = models.PositiveIntegerField(default=100)
    phone_number =models.PositiveIntegerField(default=254799735661)

    def __str__(self):
        return f'{self.name} payment'

    def save_payment(self):
        self.save()

        
class Tourguide(models.Model):

    name = models.CharField(max_length =30)
    images = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name

    def save_tourguide(self):
        self.save()


