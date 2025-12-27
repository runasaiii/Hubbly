# DRF
from rest_framework.test import APIClient
from rest_framework import status

# Python modules
from uuid import uuid4

# Django modules
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
            password='testpass123'
        )
        
        self.notification = Notification.objects.create(user=self.user)
        
        self.client.force_authenticate(user=self.user)
        self.list_url = '/notification/'

    # GET
    def test_list_notifications_success(self):
        """Good case: successfully get list of notifications for authenticated user"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.notification.id)

    def test_list_notifications_unauthorized(self):
        """Bad case 1: try to list notifications without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_notifications_wrong_method(self):
        """Bad case 2: wrong HTTP method (PUT instead of GET)"""
        response = self.client.put(self.list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_notifications_isolation(self):
        """Bad case 3: uer shouldnt see other users notifications"""
        other_user = CustomUser.objects.create_user(username='other', password='123')
        Notification.objects.create(user=other_user)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)


    # POST
    def test_create_notification_success(self):
        """Good case: successfully create notification"""
        data = {
            'user': self.user.id,
            'message': 'Test notification'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notification.objects.filter(id=response.data['id']).exists())

    def test_create_notification_unauthorized(self):
        """Bad case 1: create notification without authentication"""
        self.client.force_authenticate(user=None)
        data = {'user': self.user.id}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_notification_empty_data(self):
        """Bad case 2: create notification with missing data"""
        data = {}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_notification_invalid_user_id(self):
        """Bad case 3: create notification with invalid uuid format"""
        data = {
            'user': 'invalid-uuid-string'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
