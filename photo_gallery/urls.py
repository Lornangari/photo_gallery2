from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('upload/', views.upload_photo_view, name='upload'),
    path('like/<int:photo_id>/', views.toggle_like_view, name='like'),


]
