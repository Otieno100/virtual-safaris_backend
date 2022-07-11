from django.contrib import admin
from .models import User, Tourist, Tourguide, Safaris
from django.contrib.auth.models import Group
from . import models

# Register your models here.

admin.site.register(User)
admin.site.register(Tourist)
admin.site.register(Safaris)
admin.site.register(Tourguide)
admin.site.register(models.Profile)

