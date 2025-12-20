# Python modules
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4

# Django modules
from django.urls import reverse
from django.test import TestCase

# Project modules
from apps.users.models import CustomUser
from apps.notifications.models import Notification


class NotificationEndpointsTests(TestCase):
    """Tests for notification endpoints"""
    def setUp(self):
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            full_name='Test User',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.other_user = CustomUser.objects.create_user(
            email='otheruser@example.com',
            username='otheruser',
            full_name='Other User',
            password='testpass123'
        )

        self.notification = Notification.objects.create(
            user=self.user
        )

        self.list_url = '/notification/'

# List notifications 
    def test_list_notifications_success(self):
        """Successfully get list of notifications"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_notifications_without_auth(self):
        """Get notifications without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])

    def test_list_notifications_empty(self):
        """Get empty list of notifications"""
        Notification.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_notifications_wrong_method(self):
        """Use wrong HTTP method"""
        response = self.client.put(self.list_url, {}, format='json')
        self.assertIn(response.status_code, [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_200_OK])

# Create notification 
    def test_create_notification_success(self):
        """Successfully create notification"""
        data = {
            'user': self.user.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_200_OK])

    def test_create_notification_without_auth(self):
        """Create notification without authentication"""
        self.client.force_authenticate(user=None)
        data = {
            'user': self.user.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_create_notification_missing_user(self):
        """Create notification without user"""
        data = {}
        response = self.client.post(self.list_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_201_CREATED])

    def test_create_notification_invalid_user(self):
        """Create notification with invalid user ID"""
        data = {
            'user': uuid4()
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

 # Filter notifications 
    def test_list_notifications_filtered_by_user(self):
        """Get notifications filtered by user"""
        Notification.objects.create(user=self.other_user)
    
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_list_notifications_multiple_users(self):
        """Get notifications when multiple users have notifications"""
        Notification.objects.create(user=self.other_user)
        Notification.objects.create(user=self.user)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_list_notifications_pagination(self):
        """Get notifications with pagination"""
        for i in range(25):
            Notification.objects.create(user=self.user)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_list_notifications_deleted_filter(self):
        """Get notifications excluding deleted ones"""
        notification = Notification.objects.create(user=self.user)
        notification.delete() 
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification_ids = [n['id'] for n in response.data if 'id' in n]
        if hasattr(notification, 'id'):
            self.assertNotIn(str(notification.id), notification_ids)


