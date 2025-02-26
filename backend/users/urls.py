from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    # User registration and management
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('list/', views.list_users, name='list_users'),
    path('<int:user_id>/', views.get_user, name='get_user'),
    path('<int:user_id>/update/', views.update_user, name='update_user'),
    path('<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # User profile
    path('profile/', views.get_my_profile, name='my_profile'),
    path('profile/update/', views.update_my_profile, name='update_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)