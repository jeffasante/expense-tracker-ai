from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo_home, name='demo_home'),
    path('login/', views.demo_login, name='demo_login'),
    path('register/', views.demo_register, name='demo_register'),
    path('logout/', views.demo_logout, name='demo_logout'),
    path('categorize/', views.demo_categorize, name='demo_categorize'),
    path('analytics/', views.demo_analytics, name='demo_analytics'),
]