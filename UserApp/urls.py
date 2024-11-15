from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('phone-login/', views.phone_login, name='phone_login'),
    path('forgot-pass/', views.forgot_password, name='forgot_pass'),
    path('reset-pass/<code>', views.reset_password, name='reset_pass'),
    path('check-login/', TokenRefreshView.as_view(), name='login_refresh'),
    path('login/', views.MyTokenObtainPairView.as_view(serializer_class=views.MyTokenObtainPairSerializer),
         name='login'),
    path('register/', views.RegisterViewDRF.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
