from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Safaris
from .serializer import SafarisSerializer
from rest_framework import status

# Create your views here.


class HelloKenya(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {
            'message':"HelloKenya"
        }
        return Response(content)
    
class Extractor(APIView):
    parser_classes = (IsAuthenticated,)
    def get(self, request):
        content = {
                'username':request.user.username,
                'password': request.user.password,
            }
        return Response(content)



class safaris(APIView):
    def get(self, request, format=None):
        safaris = Safaris.objects.all()
        serializers = SafarisSerializer(safaris, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = SafarisSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    