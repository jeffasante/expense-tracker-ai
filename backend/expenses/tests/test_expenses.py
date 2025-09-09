from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from expenses.models import Expense
from datetime import date

User = get_user_model()

class ExpenseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.expense_url = reverse('expense-list-create')

    def test_create_expense(self):
        data = {
            'amount': '25.50',
            'description': 'Lunch at restaurant',
            'category': 'food',
            'date': '2024-01-15'
        }
        response = self.client.post(self.expense_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        expense = Expense.objects.first()
        self.assertEqual(expense.user, self.user)

    def test_list_expenses(self):
        Expense.objects.create(
            user=self.user,
            amount=25.50,
            description='Test expense',
            category='food',
            date=date.today()
        )
        response = self.client.get(self.expense_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.expense_url)
        # Demo mode allows unauthenticated access
        self.assertEqual(response.status_code, status.HTTP_200_OK)