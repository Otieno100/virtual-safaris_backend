from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *
from safaris.views import TourguideOnlyView, TouristOnlyView, TouristSignupView, TourguideSignupView, CustomAuthToken, LogoutView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns =[
    path('',views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/tourist/', TouristSignupView.as_view()),
    path('register/tourguide/', TourguideSignupView.as_view()),
    path('login/', CustomAuthToken.as_view(), name="auth_token"),
    path('tourist/dashboard/', TouristOnlyView.as_view(), name="tourist_dashboard"),
    path('employer/dashboard/', TourguideOnlyView.as_view(), name="tourguide_dashboard"),
   
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)