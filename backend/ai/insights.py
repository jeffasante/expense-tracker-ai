from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from expenses.models import Expense

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("NumPy not available, using basic statistics")

class InsightsGenerator:
    def __init__(self, user):
        self.user = user

    def get_monthly_summary(self, year=None, month=None):
        if not year or not month:
            now = timezone.now()
            year, month = now.year, now.month

        expenses = Expense.objects.filter(
            user=self.user,
            date__year=year,
            date__month=month
        )

        return {
            'total_amount': expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_expenses': expenses.count(),
            'average_expense': expenses.aggregate(Avg('amount'))['amount__avg'] or 0,
            'by_category': list(expenses.values('category').annotate(
                total=Sum('amount'),
                count=Count('id')
            ).order_by('-total'))
        }

    def get_top_categories(self, days=30):
        start_date = timezone.now().date() - timedelta(days=days)
        expenses = Expense.objects.filter(
            user=self.user,
            date__gte=start_date
        )

        return list(expenses.values('category').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')[:5])

    def detect_anomalies(self, days=30):
        start_date = timezone.now().date() - timedelta(days=days)
        expenses = Expense.objects.filter(
            user=self.user,
            date__gte=start_date
        ).values_list('amount', flat=True)

        if len(expenses) < 3:
            return []

        amounts = [float(amount) for amount in expenses]
        
        if NUMPY_AVAILABLE:
            mean_amount = float(np.mean(amounts))
            std_amount = float(np.std(amounts))
        else:
            # Basic statistics without numpy
            mean_amount = sum(amounts) / len(amounts)
            variance = sum((x - mean_amount) ** 2 for x in amounts) / len(amounts)
            std_amount = variance ** 0.5
            
        # Lower threshold for demo purposes to catch high-value expenses
        threshold = mean_amount + (1.5 * std_amount) if std_amount > 0 else mean_amount * 2

        anomalous_expenses = Expense.objects.filter(
            user=self.user,
            date__gte=start_date,
            amount__gt=threshold
        ).values('id', 'description', 'amount', 'date')

        return list(anomalous_expenses)

    def get_spending_trends(self, weeks=4):
        trends = []
        for i in range(weeks):
            start_date = timezone.now().date() - timedelta(weeks=i+1)
            end_date = timezone.now().date() - timedelta(weeks=i)
            
            week_total = Expense.objects.filter(
                user=self.user,
                date__gte=start_date,
                date__lt=end_date
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            trends.append({
                'week': f"Week {i+1}",
                'total': float(week_total),
                'start_date': start_date,
                'end_date': end_date
            })
        
        return trends