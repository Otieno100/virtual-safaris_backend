from django.urls.conf import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('api/profile', views.ProfileList.as_view()),

    path('account/', include('django.contrib.auth.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)