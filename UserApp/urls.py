from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(serializer_class=views.MyTokenObtainPairSerializer),
         name='login'),
    path('register/', views.RegisterViewDRF.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user-status/', views.UserStatusView.as_view()),  # Class-based view

]
