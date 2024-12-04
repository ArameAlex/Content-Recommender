from django.urls import path

from ContentApp import views

urlpatterns = [
    path('', views.home, name='content_page'),
]
