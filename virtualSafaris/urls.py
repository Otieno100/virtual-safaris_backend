from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('safaris.urls')),
    path('api/', include('safaris.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
   
]
  
   
   
    



