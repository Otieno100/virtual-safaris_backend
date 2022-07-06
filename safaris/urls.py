from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login',jwt_views.TokenObtainPairView.as_view(),name = 'login'),
    path('run',views.HelloKenya.as_view(),name = 'HelloKenya'),
    path('me',views.Extractor.as_view(),name = 'extract-token'),
    path('api/safaris', views.safaris.as_view()),
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa/<phonenumber>/<amount>/', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


