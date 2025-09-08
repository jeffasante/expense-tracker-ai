from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo_home, name='demo_home'),
    path('categorize/', views.demo_categorize, name='demo_categorize'),
    path('analytics/', views.demo_analytics, name='demo_analytics'),
]