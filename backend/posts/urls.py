from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.list_posts, name="list_posts"),
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/<int:post_id>/", views.get_post, name="get_post"),
    path('follow/', views.follow_user, name='follow_user'),
    path('follow/status/', views.follow_status, name='follow_status'),
    path("me/", views.current_user, name="current_user"),
    path('follow/followers/<str:email>/', views.get_followers, name='get_followers'),
    path('user/<str:email>/', views.get_user_posts, name='get_user_posts'),
    path("posts/<int:post_id>/update/", views.update_post, name="update_post"),
    path("posts/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path('follow/followers/<str:email>/', views.get_followers, name='get_followers'),
    path('follow/following/<str:email>/', views.get_following, name='get_following'),

]