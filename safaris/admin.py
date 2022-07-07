from django.contrib import admin
from .models import Safaris, Tourguide


# Register your models here.
admin.site.register(Safaris)
admin.site.register(Tourguide)

from .models import Profile

admin.site.register(Profile)
