from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services.categorization_service import CategorizationService
from .insights import InsightsGenerator
from expenses.models import Expense

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def categorize_expense(request):
    """
    Categorize expense description using AI.
    
    Uses rule-based keyword matching to predict the most appropriate category
    for an expense based on its description. Returns the predicted category,
    confidence score, and method used.
    
    **Supported Categories:**
    - food, transport, shopping, entertainment, bills, healthcare, education, travel, other
    
    **AI Methods:**
    - rule_based: Keyword matching (primary method)
    - fallback: Default when no keywords match
    
    **Request Body:**
    - description (string, required): Expense description to categorize
    
    **Response:**
    - predicted_category: AI-predicted category
    - confidence: Confidence score (0.0-1.0)
    - method: AI method used
    - matched_keyword: Keyword that triggered categorization (if any)
    """
    description = request.data.get('description')
    if not description:
        return Response({'error': 'Description is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)

    service = CategorizationService()
    result = service.categorize(description)
    
    return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def auto_categorize_expense(request):
    """Auto-categorize existing expense with AI"""
    expense_id = request.data.get('expense_id')
    if not expense_id:
        return Response({'error': 'expense_id is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)

    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
    except Expense.DoesNotExist:
        return Response({'error': 'Expense not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

    service = CategorizationService()
    result = service.categorize(expense.description)
    
    # Store AI prediction (user can override manually)
    expense.ai_predicted_category = result['predicted_category']
    expense.save()
    
    return Response({
        'expense_id': expense.id,
        'ai_predicted_category': result['predicted_category'],
        'current_category': expense.category,
        'confidence': result['confidence'],
        'method': result['method']
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def override_ai_category(request):
    """
    Manually override AI category prediction.
    
    Allows users to correct AI predictions while preserving the original
    AI suggestion for learning purposes. This enables continuous improvement
    of the AI model by tracking user corrections.
    
    **Use Cases:**
    - Correct misclassified expenses
    - Handle edge cases AI doesn't recognize
    - Provide user control over categorization
    
    **Request Body:**
    - expense_id (integer, required): ID of expense to update
    - category (string, required): New category from valid choices
    
    **Valid Categories:**
    food, transport, shopping, entertainment, bills, healthcare, education, travel, other
    
    **Response:**
    - expense_id: Updated expense ID
    - old_category: Previous category
    - new_category: New user-selected category
    - ai_predicted_category: Original AI prediction (preserved)
    - override_applied: Confirmation boolean
    
    **Error Cases:**
    - 400: Missing required fields or invalid category
    - 404: Expense not found or not owned by user
    """
    expense_id = request.data.get('expense_id')
    new_category = request.data.get('category')
    
    if not expense_id or not new_category:
        return Response({'error': 'expense_id and category are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)

    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
    except Expense.DoesNotExist:
        return Response({'error': 'Expense not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

    # Validate category choice
    valid_categories = [choice[0] for choice in Expense.CATEGORY_CHOICES]
    if new_category not in valid_categories:
        return Response({'error': f'Invalid category. Must be one of: {valid_categories}'}, 
                       status=status.HTTP_400_BAD_REQUEST)

    # Store original AI prediction and user override
    old_category = expense.category
    expense.category = new_category
    expense.save()
    
    return Response({
        'expense_id': expense.id,
        'old_category': old_category,
        'new_category': new_category,
        'ai_predicted_category': expense.ai_predicted_category,
        'override_applied': True
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_insights(request):
    """
    Get comprehensive AI-powered spending insights and analytics.
    
    Provides personalized financial insights using statistical analysis
    and machine learning techniques to help users understand their
    spending patterns and identify potential issues.
    
    **Monthly Summary:**
    - Total spending amount and expense count
    - Average expense calculation
    - Category-wise breakdown with totals and counts
    
    **Top Categories (Last 30 Days):**
    - Categories ranked by total spending amount
    - Limited to top 5 categories for focus
    - Includes both amount and transaction count
    
    **AI Anomaly Detection:**
    - Statistical analysis using z-score method (2-sigma rule)
    - Identifies expenses significantly above user's historical average
    - Helps detect unusual spending patterns or potential fraud
    - Requires minimum 3 expenses for statistical validity
    
    **Spending Trends (Last 4 Weeks):**
    - Week-over-week spending analysis
    - Shows spending patterns and trends over time
    - Helps identify spending increases or decreases
    
    **Query Parameters:**
    - year (optional): Specific year for monthly summary
    - month (optional): Specific month for monthly summary
    - If not provided, uses current month
    
    **Response Structure:**
    All insights are personalized to the authenticated user and
    include only their expense data for privacy and relevance.
    """
    generator = InsightsGenerator(request.user)
    
    # Get query parameters
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year and month:
        monthly_summary = generator.get_monthly_summary(int(year), int(month))
    else:
        monthly_summary = generator.get_monthly_summary()
    
    insights = {
        'monthly_summary': monthly_summary,
        'top_categories': generator.get_top_categories(),
        'anomalies': generator.detect_anomalies(),
        'spending_trends': generator.get_spending_trends()
    }
    
    return Response(insights)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_supported_categories(request):
    """Get list of supported AI categories"""
    service = CategorizationService()
    categories = service.get_categories()
    
    return Response({
        'supported_categories': categories,
        'total_count': len(categories)
    })