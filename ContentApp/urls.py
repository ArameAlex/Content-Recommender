from django.urls import path

from ContentApp import views

urlpatterns = [
    path('', views.home, name='content_page'),
    path('posts/<int:id>/', views.single_content, name='single_post_page'),
]
