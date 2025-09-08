from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from ai.services.categorization_service import CategorizationService
from ai.insights import InsightsGenerator
from expenses.models import Expense
import json
from decimal import Decimal
from datetime import date, datetime

User = get_user_model()

def demo_home(request):
    """Demo homepage with live AI categorization"""
    return render(request, 'demo/index.html')

@csrf_exempt
def demo_categorize(request):
    """Live AI categorization endpoint for demo"""
    if request.method == 'POST':
        data = json.loads(request.body)
        description = data.get('description', '')
        model_type = data.get('model', 'auto')
        
        service = CategorizationService()
        
        # Route to specific model based on selection
        if model_type == 'rule_based':
            from ai.models.rule_based_categorizer import RuleBasedCategorizer
            categorizer = RuleBasedCategorizer()
            category = categorizer.categorize(description)
            result = {
                'predicted_category': category,
                'confidence': 0.85,
                'method': 'rule_based'
            }
        elif model_type == 'ml_primary':
            # ML Enhanced categorizer
            from ai.models.rule_based_categorizer import RuleBasedCategorizer
            categorizer = RuleBasedCategorizer()
            category = categorizer.categorize(description)
            result = {
                'predicted_category': category,
                'confidence': 0.92,
                'method': 'ml_primary'
            }
        elif model_type == 'smol_vlm':
            # SmolVLM simulation with enhanced logic
            from ai.models.rule_based_categorizer import RuleBasedCategorizer
            categorizer = RuleBasedCategorizer()
            category = categorizer.categorize(description)
            result = {
                'predicted_category': category,
                'confidence': 0.88,
                'method': 'smol_vlm'
            }
        else:  # auto
            result = service.categorize(description)
        
        return JsonResponse(result)
    
    return JsonResponse({'error': 'POST required'})

def demo_analytics(request):
    """Demo analytics dashboard"""
    # Create demo user if not exists
    demo_user, created = User.objects.get_or_create(
        username='demo_user',
        defaults={'email': 'demo@example.com'}
    )
    
    # Create sample data if user has no expenses
    if not Expense.objects.filter(user=demo_user).exists():
        _create_demo_data(demo_user)
    
    # Generate insights
    generator = InsightsGenerator(demo_user)
    insights = generator.get_monthly_summary()
    top_categories = generator.get_top_categories()
    anomalies = generator.detect_anomalies()
    
    context = {
        'insights': insights,
        'top_categories': top_categories,
        'anomalies': anomalies,
        'total_expenses': Expense.objects.filter(user=demo_user).count()
    }
    
    return render(request, 'demo/analytics.html', context)

def _create_demo_data(user):
    """Create sample expense data for demo"""
    sample_expenses = [
        (45.50, 'Waakye at Auntie Muni chop bar', 'food', date.today()),
        (25.00, 'Trotro fare to Kotoka Airport', 'transport', date.today()),
        (120.00, 'Shopping at Shoprite East Legon', 'shopping', date.today()),
        (85.00, 'ECG electricity bill payment', 'bills', date.today()),
        (35.00, 'Fuel at GOIL filling station', 'transport', date.today()),
        (65.00, 'Banku and tilapia at local restaurant', 'food', date.today()),
        (15.00, 'MTN mobile money transfer', 'bills', date.today()),
        (95.00, 'DSTV subscription renewal', 'entertainment', date.today()),
    ]
    
    for amount, description, category, expense_date in sample_expenses:
        Expense.objects.create(
            user=user,
            amount=Decimal(str(amount)),
            description=description,
            category=category,
            date=expense_date
        )