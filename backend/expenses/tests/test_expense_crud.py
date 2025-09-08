from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from expenses.models import Expense
from datetime import date
from decimal import Decimal

User = get_user_model()

class ExpenseCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_expense_complete(self):
        """Test creating expense with all required fields"""
        data = {
            'amount': '285.50',
            'description': 'Grocery shopping at Shoprite',
            'category': 'food',
            'date': '2024-01-15'
        }
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        expense = Expense.objects.get(id=response.data['id'])
        self.assertEqual(expense.amount, Decimal('285.50'))
        self.assertEqual(expense.user, self.user)

    def test_update_expense(self):
        """Test updating existing expense"""
        expense = Expense.objects.create(
            user=self.user,
            amount=58.00,
            description='Original description',
            category='food',
            date=date.today()
        )
        
        data = {
            'amount': '81.50',
            'description': 'Updated description',
            'category': 'transport',
            'date': '2024-01-16'
        }
        response = self.client.put(f'/api/expenses/{expense.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expense.refresh_from_db()
        self.assertEqual(expense.amount, Decimal('81.50'))
        self.assertEqual(expense.description, 'Updated description')

    def test_delete_expense(self):
        """Test deleting expense"""
        expense = Expense.objects.create(
            user=self.user,
            amount=58.00,
            description='Test expense',
            category='food',
            date=date.today()
        )
        
        response = self.client.delete(f'/api/expenses/{expense.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=expense.id).exists())

    def test_user_isolation(self):
        """Test users can only access their own expenses"""
        other_expense = Expense.objects.create(
            user=self.other_user,
            amount=100.00,
            description='Other user expense',
            category='food',
            date=date.today()
        )
        
        # Try to access other user's expense
        response = self.client.get(f'/api/expenses/{other_expense.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_expense_filtering(self):
        """Test filtering expenses by category and date"""
        Expense.objects.create(user=self.user, amount=58.00, description='Waakye', category='food', date=date(2024, 1, 15))
        Expense.objects.create(user=self.user, amount=34.00, description='Trotro fare', category='transport', date=date(2024, 1, 15))
        Expense.objects.create(user=self.user, amount=79.50, description='Banku and tilapia', category='food', date=date(2024, 1, 16))
        
        # Filter by category
        response = self.client.get('/api/expenses/?category=food')
        self.assertEqual(len(response.data), 2)
        
        # Filter by date
        response = self.client.get('/api/expenses/?date=2024-01-15')
        self.assertEqual(len(response.data), 2)