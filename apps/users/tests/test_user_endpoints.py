# DRF
from rest_framework.test import APIClient
from rest_framework import status

# Django modules
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

# project modules
from apps.users.models import CustomUser


class UserEndpointTests(TestCase):
    """Test for user endpoints"""

    def setUp(self):
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

    def test_login_success(self):
        """Successful login test returns tokens"""
        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_email(self):
        """Login with wrong email test"""
        response = self.client.post(self.login_url, {
            "email": "wrong@example.com",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        """Login with wrong password test"""
        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "wrongpassword"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_empty_payload(self):
        """Login with empty payload test"""
        response = self.client.post(self.login_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
    
    def test_register_missing_fields(self):
        """Registration with missing fields test"""
        response = self.client.post(self.register_url, {
            "email": "test2@example.com",
            "full_name": "New",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_email(self):
        """Registration with invalid email test"""
        response = self.client.post(self.register_url, {
            "email": "invalid-email",
            "username": "someuser",
            "full_name": "Some User",
            "password": "testpass123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_personal_data_success(self):
        """Successful retrieval of personal data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.personal_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "test@example.com")

    def test_personal_data_without_token(self):
        """Retrieval of personal data without token test"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.personal_data_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_personal_data_wrong_method_post(self):
        """Use wrong http method post on personal data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.personal_data_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_personal_data_wrong_method_delete(self):
        """Use wrong http method delete on personal data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.personal_data_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_profile_patch_success(self):
        """Successful profile update"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.profile_url, {
            "bio": "Updated bio",
            "location": "New York"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], "Updated bio")

    def test_profile_patch_without_auth(self):
        """Update profile without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.profile_url, {
            "bio": "Updated bio"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_patch_invalid_data(self):
        """Update profile with invalid data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.profile_url, {
            "gender": "invalid_gender" 
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_delete_not_allowed(self):
        """Delete profile not allowed"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_avatar_upload_success(self):
        """Successful avatar upload"""
        self.client.force_authenticate(user=self.user)
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
        self.client.force_authenticate(user=None)
        response = self.client.post(self.avatar_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_avatar_upload_no_file(self):
        """Upload avatar without file"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.avatar_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_avatar_upload_invalid_file(self):
        """Upload avatar with invalid file type"""
        self.client.force_authenticate(user=self.user)
        uploaded_file = SimpleUploadedFile(
            "document.pdf",
            b"fake pdf content",
            content_type="application/pdf"
        )
        response = self.client.post(self.avatar_url, {
            "avatar": uploaded_file
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_list_success(self):
        """Successful retrieval of user list"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_user_list_wrong_method_put(self):
        """Use wrong http method put on list"""
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.user_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_list_wrong_method_delete(self):
        """Use wrong http method delete on list"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_list_wrong_method_patch(self):
        """Use wrong http method patch on list"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.user_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_detail_success(self):
        """Successful retrieval of user detail"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['email'], "test@example.com")

    def test_user_detail_not_found(self):
        """Get user detail with non-existent id"""
        self.client.force_authenticate(user=self.user)
        invalid_url = "/users/api/99999/"
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_wrong_method_post(self):
        """Use wrong http method post on detail"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.user_detail_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_detail_wrong_method_delete(self):
        """Use wrong http method delete on detail"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)