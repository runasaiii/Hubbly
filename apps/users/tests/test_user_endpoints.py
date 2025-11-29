# Python modules
from rest_framework.test import APIClient
from rest_framework import status

# Django modules
from django.urls import reverse
from django.test import TestCase

# Project modules
from apps.users.models import CustomUser


class UserEndpointTests(TestCase):
    """Test for user endpoints"""

    def setUp(self):
        """Set up test data"""

        self.client = APIClient()
        
        self.user = CustomUser.objects.create_user(
            email = "test@example.com",
            username = "testuser",
            full_name = "Test User",
            password = "12345"
        )

        self.login_url = "/users/v1/user/login"
        self.register_url = "/users/v1/user/register"
        self.personal_data_url = "/users/v1/user/personal_data"

# Login test
        def test_login_succes(self):
            """Successful login test - returns tokens"""
            response = self.client.post(self.login_url, {
                "email": "test@example.com",
                "password": "12345"
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('access', response.data)
            self.assertIn('refresh', response.data)
            self.assertEqual(response.data['email'], "test@example.com")
        
        def test_login_wrong_email(self):
            """Login with wrong email test"""
            response = self.client.post(self.login_url, {
                "email": "kate@example.com",
                "password": "12345"
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('email', response.data)

        def test_login_wrong_password(self):
            """Login with wrong password test"""
            response = self.client.post(self.login_url, {
                "email": "test@example.com",
                "password": "kate123"
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('password', response.data)

        def test_login_empty_payload(self):
            """Login with empty payload test"""
            response = self.client.post(self.login_url, {}, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('email', response.data)
            self.assertIn('password', response.data)

# egister test
        def test_register_success(self):
            """Successful user registration"""
            response = self.client.post(self.register_url, {
                "email": "newuser@example.com",
                "username": "newuser",
                "full_name": "New User",
                "password": "12345"
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn("access", response.data)
            self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

        def test_register_existing_email(self):
            """Registration with existing email test"""
            response = self.client.post(self.register_url, {
                "email": "test@example.com",
                "username": "anotheruser",
                "full_name": "Another User",
                "password": "12345"
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('email', response.data)
        
        def test_register_missing_fields(self):
            """Registration with missing fields test"""
            response = self.client.post(self.register_url, {
                "email": "test2@example.com",
                "full_name": "New",
                "password": "12345"
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('username', response.data)

        def test_register_invalid_email(self):
            """Registration with invalid email test"""
            response = self.client.post(self.register_url, {
                "email": "abcde",
                "username": "someuser",
                "full_name": "Some User",
                "password": "12345"
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('email', response.data)

# Personal data tests
        def test_personal_data_success(self):
            """Successful retrieval of personal data"""
            login = self.client.post(self.login_url, {
                "email": "test@example.com",
                "password": "12345"
            }, format='json')

            token = login.data['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

            response = self.client.get(self.personal_data_url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['email'], "test@example.com")


        def personal_data_without_token(self):
            """Retrieval of personal data without token test"""
            response = self.client.get(self.personal_data_url)

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        def test_personal_data_invalid_token(self):
            """Retrieval of personal data with invalid token test"""
            self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken123')
            response = self.client.get(self.personal_data_url)

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        def test_personal_data_wrong_token_type(self):
            """Wrong auto headers format"""
            self.client.credentials(HTTP_AUTHORIZATION='Token abc123')

            response = self.client.get(self.personal_data_url)

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)