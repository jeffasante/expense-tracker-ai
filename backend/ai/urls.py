from django.urls import path
from . import views

urlpatterns = [
    path('categorize/', views.categorize_expense, name='categorize-expense'),
    path('auto-categorize/', views.auto_categorize_expense, name='auto-categorize-expense'),
    path('override-category/', views.override_ai_category, name='override-ai-category'),
    path('insights/', views.get_insights, name='get-insights'),
    path('categories/', views.get_supported_categories, name='supported-categories'),
]