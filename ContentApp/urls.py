from django.urls import path

from ContentApp import views

urlpatterns = [
    path('', views.home, name='content_page'),
    path('posts/<int:content_id>/', views.single_content, name='single_post_page'),
    path('saved-contents/', views.saved_contents, name='saved_contents'),
    path('saved-contents/delete/<int:content_id>', views.unsaved_contents, name='unsaved_contents'),
]
