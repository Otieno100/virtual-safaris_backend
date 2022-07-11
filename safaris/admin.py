from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group


# Register your models here.
admin.site.register(User)
admin.site.register(Tourist)
admin.site.register(Safaris)
admin.site.register(Tourguide)
admin.site.register(Profile)

