from .models import *
from rest_framework import serializers


class TourguideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourguide
        fields = ('image', 'name')