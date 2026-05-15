from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('create/', views.create_post, name='create-post'),
    path('<int:post_id>/like/', views.toggle_like, name='toggle-like'),
    path('<int:post_id>/delete/', views.delete_post, name='post-delete'),
    path('<int:post_id>/comments/', views.post_comments, name='post-comments'),
    path('<int:post_id>/comment/', views.create_comment, name='create-comment'),
]
