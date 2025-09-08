import os
import sys
import django
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from expenses.models import Expense
from datetime import date

User = get_user_model()

class EndToEndTestCase(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_complete_workflow(self):
        # 1. Register user
        register_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post('/api/auth/register/', register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        access_token = response.data['access']

        # 2. Set authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 3. Create expense
        expense_data = {
            'amount': '58.00',
            'description': 'Waakye at chop bar',
            'category': 'food',
            'date': '2024-01-15'
        }
        response = self.client.post('/api/expenses/', expense_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expense_id = response.data['id']

        # 4. Test AI categorization
        categorize_data = {'description': 'Uber ride to airport'}
        response = self.client.post('/api/ai/categorize/', categorize_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['predicted_category'], 'transport')

        # 5. Auto-categorize existing expense
        auto_categorize_data = {'expense_id': expense_id}
        response = self.client.post('/api/ai/auto-categorize/', auto_categorize_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 6. Manual override AI category
        override_data = {'expense_id': expense_id, 'category': 'entertainment'}
        response = self.client.post('/api/ai/override-category/', override_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['override_applied'])

        # 7. Get supported categories
        response = self.client.get('/api/ai/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('supported_categories', response.data)

        # 8. Get insights
        response = self.client.get('/api/ai/insights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('monthly_summary', response.data)

        # 9. List expenses
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)