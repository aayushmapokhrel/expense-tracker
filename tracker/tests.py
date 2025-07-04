from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import ExpenseIncome

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class ExpenseIncomeTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.superuser = User.objects.create_superuser(username='admin', password='admin123')
        
        self.expense1 = ExpenseIncome.objects.create(
            user=self.user1,
            title='Test Expense 1',
            amount=100.00,
            transaction_type='debit',
            tax=10.00,
            tax_type='flat'
        )
        
        self.client = APIClient()

    def test_create_expense(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Expense',
            'amount': 50.00,
            'transaction_type': 'debit',
            'tax': 5.00,
            'tax_type': 'flat'
        }
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Expense')

    def test_user_cannot_access_other_users_data(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/expenses/{self.expense1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_access_all_data(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(f'/api/expenses/{self.expense1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Expense 1')

    def test_tax_calculation_flat(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Flat Tax Test',
            'amount': 100.00,
            'transaction_type': 'debit',
            'tax': 10.00,
            'tax_type': 'flat'
        }
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total'], '110.00')

    def test_tax_calculation_percentage(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Percentage Tax Test',
            'amount': 100.00,
            'transaction_type': 'debit',
            'tax': 10.00,
            'tax_type': 'percentage'
        }
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total'], '110.00')