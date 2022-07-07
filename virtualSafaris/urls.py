
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('safaris.urls')),
    
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
 
    path('api/', include('safaris.api.urls')),
]




