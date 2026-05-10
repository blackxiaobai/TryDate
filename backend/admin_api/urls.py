from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='admin-dashboard'),
    path('users/', views.user_list, name='admin-users'),
    path('users/<uuid:user_id>/ban/', views.ban_user, name='admin-ban-user'),
    path('users/<uuid:user_id>/unban/', views.unban_user, name='admin-unban-user'),
    path('matches/', views.match_list, name='admin-matches'),
    path('posts/', views.post_list, name='admin-posts'),
    path('posts/<int:post_id>/hide/', views.hide_post, name='admin-hide-post'),
    path('posts/<int:post_id>/restore/', views.restore_post, name='admin-restore-post'),
    path('reports/', views.report_list, name='admin-reports'),
    path('reports/<int:report_id>/resolve/', views.resolve_report, name='admin-resolve-report'),
]
