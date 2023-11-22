from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_home, name='home'),
    path('homepage/', views.home, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Add other URLs for your app as needed
]