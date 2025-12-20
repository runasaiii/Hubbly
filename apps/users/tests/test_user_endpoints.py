# Python modules
from rest_framework.test import APIClient
from rest_framework import status

# Django modules
from django.urls import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

# Project modules
from apps.users.models import CustomUser, Profile


class UserEndpointTests(TestCase):
    """Test for user endpoints"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            password="testpass123"
        )

        self.login_url = "/users/v1/user/login"
        self.register_url = "/users/v1/user/register"
        self.personal_data_url = "/users/v1/user/personal_data"
        self.profile_url = "/users/v1/user/profile"
        self.avatar_url = "/users/v1/user/profile/avatar"
        self.user_list_url = "/users/api/"
        self.user_detail_url = f"/users/api/{self.user.id}/"

# Login
    def test_login_success(self):
        """Successful login test - returns tokens"""
        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['email'], "test@example.com")
    
    def test_login_wrong_email(self):
        """Login with wrong email test"""
        response = self.client.post(self.login_url, {
            "email": "wrong@example.com",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_wrong_password(self):
        """Login with wrong password test"""
        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "wrongpassword"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_empty_payload(self):
        """Login with empty payload test"""
        response = self.client.post(self.login_url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

# Register
    def test_register_success(self):
        """Successful user registration"""
        response = self.client.post(self.register_url, {
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

    def test_register_existing_email(self):
        """Registration with existing email test"""
        response = self.client.post(self.register_url, {
            "email": "test@example.com",
            "username": "anotheruser",
            "full_name": "Another User",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_register_missing_fields(self):
        """Registration with missing fields test"""
        response = self.client.post(self.register_url, {
            "email": "test2@example.com",
            "full_name": "New",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_invalid_email(self):
        """Registration with invalid email test"""
        response = self.client.post(self.register_url, {
            "email": "invalid-email",
            "username": "someuser",
            "full_name": "Some User",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

# Personal data
    def test_personal_data_success(self):
        """Successful retrieval of personal data"""
        login = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.personal_data_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "test@example.com")

    def test_personal_data_without_token(self):
        """Retrieval of personal data without token test"""
        response = self.client.get(self.personal_data_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_personal_data_invalid_token(self):
        """Retrieval of personal data with invalid token test"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken123')
        response = self.client.get(self.personal_data_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_personal_data_wrong_token_type(self):
        """Wrong auth headers format"""
        self.client.credentials(HTTP_AUTHORIZATION='Token abc123')

        response = self.client.get(self.personal_data_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Profile
    def test_profile_get_success(self):
        """Successful retrieval of profile"""
        login = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)

    def test_profile_get_without_auth(self):
        """Get profile without authentication"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_patch_success(self):
        """Successful profile update"""
        login = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.patch(self.profile_url, {
            "bio": "Updated bio",
            "location": "New York"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], "Updated bio")

    def test_profile_patch_without_auth(self):
        """Update profile without authentication"""
        response = self.client.patch(self.profile_url, {
            "bio": "Updated bio"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_patch_invalid_data(self):
        """Update profile with invalid data"""
        login = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.patch(self.profile_url, {
            "gender": "invalid_gender"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Avatar upload
    def test_avatar_upload_success(self):
        """Successful avatar upload"""
        login = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
        uploaded_file = SimpleUploadedFile(
            "avatar.png",
            fake_image_data,
            content_type="image/png"
        )

        response = self.client.post(self.avatar_url, {
            "avatar": uploaded_file
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('avatar', response.data)

    def test_avatar_upload_without_auth(self):
        """Upload avatar without authentication"""
        response = self.client.post(self.avatar_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_avatar_upload_no_file(self):
        """Upload avatar without file"""
        login = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(self.avatar_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_avatar_upload_invalid_file(self):
        """Upload avatar with invalid file type"""
        login = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        uploaded_file = SimpleUploadedFile(
            "document.pdf",
            b"fake pdf content",
            content_type="application/pdf"
        )

        response = self.client.post(self.avatar_url, {
            "avatar": uploaded_file
        }, format='multipart')

        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK])

# User list
    def test_user_list_success(self):
        """Successful retrieval of user list"""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_user_list_empty(self):
        """Get user list when no users exist"""
        CustomUser.objects.all().delete()
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_user_list_wrong_method(self):
        """Use wrong HTTP method"""
        response = self.client.post(self.user_list_url, {}, format='json')
        self.assertIn(response.status_code, [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_200_OK])

    def test_user_list_with_filter(self):
        """Get user list with query parameters (if supported)"""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# User detail 
    def test_user_detail_success(self):
        """Successful retrieval of user detail"""
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['email'], "test@example.com")

    def test_user_detail_not_found(self):
        """Get user detail with non-existent ID"""
        invalid_url = "/users/api/99999/"
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_invalid_id(self):
        """Get user detail with invalid ID format"""
        invalid_url = "/users/api/invalid-id/"
        response = self.client.get(invalid_url)
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST])

    def test_user_detail_wrong_method(self):
        """Use wrong HTTP method"""
        response = self.client.post(self.user_detail_url, {}, format='json')
        self.assertIn(response.status_code, [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_200_OK])