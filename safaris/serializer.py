from rest_framework import serializers
from .models import Safaris

class SafarisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Safaris
        fields = ('name', 'description', 'location', 'pub_date','image')