from rest_framework import serializers
from .models import Safaris, Tourguide

class SafarisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Safaris
        fields = ('name', 'description', 'location', 'pub_date','image')


class TourguideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourguide
        fields = ('image', 'name')