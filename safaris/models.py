from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    location = models.CharField(max_length=60, blank=True)
    phone_number = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    @classmethod
    def get_user_profile(cls, user):
        profile = cls.objects.filter(user=user)
        return profile

    def __str__(self):
        return self.user.username