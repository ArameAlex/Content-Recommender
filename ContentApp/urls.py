from django.urls import path

from ContentApp import views

urlpatterns = [
    path('', views.home, name='content_page'),
    path('posts/<int:content_id>/', views.single_content, name='single_post_page'),
    path('saved-contents/', views.saved_contents, name='saved_contents'),
    path('saved-contents/delete/<int:content_id>/', views.unsaved_contents, name='unsaved_contents'),
    path('comment/<int:content_id>/', views.create_comment_view, name='create_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/update/<int:pk>/', views.ProgramCommentView.as_view(), name='update_comment'),
]
