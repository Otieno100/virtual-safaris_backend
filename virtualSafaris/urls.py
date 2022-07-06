
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('safaris.urls')),
=======
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('', include('safaris.urls')),
    path('api/', include('safaris.api.urls')),

>>>>>>> f4622ffa1b2d2c953df550eeffd57f7747a459f3
]

