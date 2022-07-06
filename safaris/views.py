from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from safaris.serializers import TourguideSerializer
from .models import *

# Create your views here.
def all_images(request):
    images = Image.my_images()
    tourguide= Tourguide.objects.all()

    if 'tourguide' in request.GET and request.GET['tourguide']:
        tourguide = request.GET.get('tourguide')


    return render (request, 'allphotos/display.html', {"images":images, "tourguide":tourguide})


class TourguideList(APIView):
    def get(self, request, format=None):
        all_projects = Tourguide.objects.all()
        serializers = TourguideSerializer(all_projects, many=True)
        return Response(serializers.data)
