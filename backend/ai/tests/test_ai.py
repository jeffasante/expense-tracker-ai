from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from expenses.models import Expense
from ai.services.categorization_service import CategorizationService
from ai.models.rule_based_categorizer import RuleBasedCategorizer
from ai.insights import InsightsGenerator
from datetime import date

User = get_user_model()

class AITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_categorize_expense_endpoint(self):
        url = reverse('categorize-expense')
        data = {'description': 'Waakye at chop bar'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('predicted_category', response.data)
        self.assertEqual(response.data['predicted_category'], 'food')
        self.assertIn('confidence', response.data)
        self.assertIn('method', response.data)

    def test_rule_based_categorizer_food(self):
        categorizer = RuleBasedCategorizer()
        result = categorizer.predict('Pizza dinner at restaurant')
        self.assertEqual(result['predicted_category'], 'food')
        self.assertGreater(result['confidence'], 0.5)
        self.assertEqual(result['method'], 'rule_based')

    def test_rule_based_categorizer_transport(self):
        categorizer = RuleBasedCategorizer()
        result = categorizer.predict('Trotro to Kotoka airport')
        self.assertEqual(result['predicted_category'], 'transport')
        self.assertIn('matched_keyword', result)

    def test_categorizer_fallback(self):
        categorizer = RuleBasedCategorizer()
        result = categorizer.predict('Random unknown expense xyz')
        self.assertEqual(result['predicted_category'], 'other')
        self.assertEqual(result['method'], 'fallback')

    def test_categorization_service(self):
        service = CategorizationService()
        result = service.categorize('Banku and tilapia')
        self.assertEqual(result['predicted_category'], 'food')
        
        categories = service.get_categories()
        self.assertIn('food', categories)
        self.assertIn('transport', categories)

    def test_auto_categorize_expense(self):
        expense = Expense.objects.create(
            user=self.user,
            amount=25.50,
            description='McDonald\'s lunch',
            category='other',
            date=date.today()
        )
        
        url = reverse('auto-categorize-expense')
        data = {'expense_id': expense.id}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ai_predicted_category'], 'food')
        
        expense.refresh_from_db()
        self.assertEqual(expense.ai_predicted_category, 'food')

    def test_manual_override_ai_category(self):
        expense = Expense.objects.create(
            user=self.user,
            amount=25.50,
            description='McDonald\'s lunch',
            category='other',
            ai_predicted_category='food',
            date=date.today()
        )
        
        url = reverse('override-ai-category')
        data = {'expense_id': expense.id, 'category': 'entertainment'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_category'], 'entertainment')
        self.assertEqual(response.data['ai_predicted_category'], 'food')
        self.assertTrue(response.data['override_applied'])
        
        expense.refresh_from_db()
        self.assertEqual(expense.category, 'entertainment')
        self.assertEqual(expense.ai_predicted_category, 'food')  # AI prediction preserved

    def test_get_supported_categories(self):
        url = reverse('supported-categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('supported_categories', response.data)
        self.assertIn('food', response.data['supported_categories'])

    def test_insights_generation(self):
        Expense.objects.create(
            user=self.user,
            amount=25.50,
            description='Test food',
            category='food',
            date=date.today()
        )
        Expense.objects.create(
            user=self.user,
            amount=15.00,
            description='Test transport',
            category='transport',
            date=date.today()
        )

        generator = InsightsGenerator(self.user)
        monthly_summary = generator.get_monthly_summary()
        
        self.assertEqual(monthly_summary['total_expenses'], 2)
        self.assertEqual(float(monthly_summary['total_amount']), 40.50)

    def test_get_insights_endpoint(self):
        url = reverse('get-insights')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('monthly_summary', response.data)
        self.assertIn('top_categories', response.data)
        self.assertIn('anomalies', response.data)