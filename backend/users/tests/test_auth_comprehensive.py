from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AuthComprehensiveTestCase(TestCase):
    """Comprehensive authentication tests"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_registration_validation(self):
        """Test registration input validation"""
        # Missing required fields
        response = self.client.post('/api/auth/register/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Password mismatch
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'different123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Invalid email format
        data = {
            'email': 'invalid-email',
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_duplicate_email_registration(self):
        """Test registration with duplicate email"""
        # Create first user
        User.objects.create_user(
            email='test@example.com',
            username='firstuser',
            password='testpass123'
        )
        
        # Try to register with same email
        data = {
            'email': 'test@example.com',
            'username': 'seconduser',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_validation(self):
        """Test login input validation"""
        # Missing credentials
        response = self.client.post('/api/auth/login/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Missing password
        response = self.client.post('/api/auth/login/', {'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_jwt_token_refresh(self):
        """Test JWT token refresh functionality"""
        # Create user and get tokens
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        refresh = RefreshToken.for_user(user)
        
        # Test token refresh
        data = {'refresh': str(refresh)}
        response = self.client.post('/api/auth/token/refresh/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_protected_endpoint_access(self):
        """Test accessing protected endpoints with/without authentication"""
        # Without authentication
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # With valid authentication
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_successful_registration_flow(self):
        """Test complete successful registration flow"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response contains required fields
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Verify user was created
        user = User.objects.get(email='newuser@example.com')
        self.assertEqual(user.username, 'newuser')
    
    def test_successful_login_flow(self):
        """Test complete successful login flow"""
        # Create user
        User.objects.create_user(
            email='logintest@example.com',
            username='loginuser',
            password='loginpass123'
        )
        
        # Login
        data = {
            'email': 'logintest@example.com',
            'password': 'loginpass123'
        }
        
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response format
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Verify user data
        self.assertEqual(response.data['user']['email'], 'logintest@example.com')