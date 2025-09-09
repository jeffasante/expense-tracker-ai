from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Expense
from .serializers import ExpenseSerializer

User = get_user_model()

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'date']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Expense.objects.filter(user=self.request.user)
        else:
            # Create session-specific demo user
            session_key = self.request.session.session_key or self.request.session.create()
            demo_email = f'demo_{session_key}@example.com'
            demo_user, created = User.objects.get_or_create(
                email=demo_email,
                defaults={
                    'username': f'demo_{session_key}',
                    'first_name': 'Demo', 
                    'last_name': 'User'
                }
            )
            return Expense.objects.filter(user=demo_user)
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Use session-specific demo user
            session_key = self.request.session.session_key or self.request.session.create()
            demo_email = f'demo_{session_key}@example.com'
            demo_user, created = User.objects.get_or_create(
                email=demo_email,
                defaults={
                    'username': f'demo_{session_key}',
                    'first_name': 'Demo', 
                    'last_name': 'User'
                }
            )
            serializer.save(user=demo_user)

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Expense.objects.filter(user=self.request.user)
        else:
            # Use session-specific demo user
            session_key = self.request.session.session_key or self.request.session.create()
            demo_email = f'demo_{session_key}@example.com'
            demo_user, created = User.objects.get_or_create(
                email=demo_email,
                defaults={
                    'username': f'demo_{session_key}',
                    'first_name': 'Demo', 
                    'last_name': 'User'
                }
            )
            return Expense.objects.filter(user=demo_user)