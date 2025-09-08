from django.test import TestCase
from django.contrib.auth import get_user_model
from expenses.models import Expense
from ai.insights import InsightsGenerator
from datetime import date, timedelta
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

class InsightsComprehensiveTestCase(TestCase):
    """Comprehensive tests for AI insights functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.generator = InsightsGenerator(self.user)
        
        # Create test data
        today = date.today()
        self._create_test_expenses(today)
    
    def _create_test_expenses(self, base_date):
        """Create deterministic test expenses"""
        expenses_data = [
            # Current month expenses - normal range 10-30
            (25.50, 'food', base_date),
            (15.00, 'transport', base_date),
            (500.00, 'shopping', base_date),  # Clear anomaly - much higher
            (12.75, 'food', base_date - timedelta(days=1)),
            (18.50, 'transport', base_date - timedelta(days=2)),
            (22.00, 'food', base_date - timedelta(days=3)),
            (16.75, 'transport', base_date - timedelta(days=4)),
            
            # Previous month expenses
            (30.00, 'food', base_date - timedelta(days=35)),
            (20.00, 'transport', base_date - timedelta(days=36)),
        ]
        
        for amount, category, expense_date in expenses_data:
            Expense.objects.create(
                user=self.user,
                amount=Decimal(str(amount)),
                description=f'Test {category} expense',
                category=category,
                date=expense_date
            )
    
    def test_monthly_summary_current_month(self):
        """Test monthly summary for current month"""
        now = timezone.now()
        summary = self.generator.get_monthly_summary(now.year, now.month)
        
        # Should include 7 current month expenses
        self.assertEqual(summary['total_expenses'], 7)
        self.assertEqual(float(summary['total_amount']), 610.50)
        
        # Check category breakdown
        categories = {item['category']: item for item in summary['by_category']}
        self.assertEqual(float(categories['shopping']['total']), 500.00)
        self.assertEqual(float(categories['food']['total']), 60.25)
    
    def test_monthly_summary_specific_month(self):
        """Test monthly summary for specific past month"""
        past_date = date.today() - timedelta(days=35)
        summary = self.generator.get_monthly_summary(past_date.year, past_date.month)
        
        # Should include 2 previous month expenses
        self.assertEqual(summary['total_expenses'], 2)
        self.assertEqual(float(summary['total_amount']), 50.00)
    
    def test_top_categories(self):
        """Test top categories calculation"""
        top_categories = self.generator.get_top_categories(days=60)  # Include all expenses
        
        # Should be ordered by total amount
        self.assertEqual(top_categories[0]['category'], 'shopping')  # $500
        self.assertEqual(top_categories[1]['category'], 'food')      # $90.25
        self.assertEqual(top_categories[2]['category'], 'transport') # $70.25
    
    def test_anomaly_detection(self):
        """Test anomaly detection algorithm"""
        anomalies = self.generator.detect_anomalies(days=30)
        
        # $500 shopping expense should be detected as anomaly
        # (significantly higher than other expenses)
        self.assertTrue(len(anomalies) > 0)
        
        # Check if the $500 expense is flagged
        anomaly_amounts = [float(a['amount']) for a in anomalies]
        self.assertIn(500.00, anomaly_amounts)
    
    def test_anomaly_detection_insufficient_data(self):
        """Test anomaly detection with insufficient data"""
        # Create new user with minimal expenses
        new_user = User.objects.create_user(
            email='minimal@example.com',
            username='minimal',
            password='testpass123'
        )
        
        # Create only 2 expenses (less than minimum of 3)
        Expense.objects.create(user=new_user, amount=25.00, description='Test', category='food', date=date.today())
        Expense.objects.create(user=new_user, amount=30.00, description='Test', category='food', date=date.today())
        
        generator = InsightsGenerator(new_user)
        anomalies = generator.detect_anomalies()
        
        # Should return empty list
        self.assertEqual(len(anomalies), 0)
    
    def test_spending_trends(self):
        """Test spending trends calculation"""
        trends = self.generator.get_spending_trends(weeks=2)
        
        self.assertEqual(len(trends), 2)
        
        # Each trend should have required fields
        for trend in trends:
            self.assertIn('week', trend)
            self.assertIn('total', trend)
            self.assertIn('start_date', trend)
            self.assertIn('end_date', trend)
    
    def test_empty_user_insights(self):
        """Test insights for user with no expenses"""
        empty_user = User.objects.create_user(
            email='empty@example.com',
            username='empty',
            password='testpass123'
        )
        
        generator = InsightsGenerator(empty_user)
        
        # Monthly summary should handle empty data
        summary = generator.get_monthly_summary()
        self.assertEqual(summary['total_expenses'], 0)
        self.assertEqual(summary['total_amount'], 0)
        
        # Top categories should be empty
        top_categories = generator.get_top_categories()
        self.assertEqual(len(top_categories), 0)
        
        # Anomalies should be empty
        anomalies = generator.detect_anomalies()
        self.assertEqual(len(anomalies), 0)