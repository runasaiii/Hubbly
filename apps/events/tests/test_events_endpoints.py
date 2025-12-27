# python modules
import uuid
from datetime import timedelta

# DRF modules
from rest_framework import status
from rest_framework.test import APITestCase

# Django modules
from django.urls import reverse
from django.utils import timezone

# Project modules
from apps.users.models import CustomUser
from apps.communities.models import Community
from apps.events.models import Event


class EventAPITestCase(APITestCase):
    """Tests for event endpoints"""
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            full_name="Test User",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.other_user = CustomUser.objects.create_user(
            email="otheruser@example.com",
            username="otheruser",
            full_name="Other User",
            password="testpass123"
        )

        self.community = Community.objects.create(
            name="Test Community",
            owner=self.user
        )

        self.event = Event.objects.create(
            title="Sample Event",
            description="This is a sample event.",
            start_at=timezone.now() + timedelta(days=1),
            end_at=timezone.now() + timedelta(days=1, hours=2),
            capacity=50,
            status="draft",
            organizer=self.user,
            community=self.community,
        )

        self.list_url = reverse('event-list')
        self.detail_url = reverse('event-detail', kwargs={'pk': self.event.id})

    def test_event_list_success(self):
        """Successfully get list of events"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_event_list_without_auth(self):
        """Get events without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_list_wrong_method_put(self):
        """Use wrong http method put on list"""
        response = self.client.put(self.list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_event_list_wrong_method_delete(self):
        """Use wrong http method delete on list"""
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_event_detail_success(self):
        """Successfully get event detail"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.event.title)

    def test_event_detail_not_found(self):
        """Get event detail with non-existent id"""
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_detail_invalid_id(self):
        """Get event detail with invalid id format"""
        response = self.client.get('/events/api/invalid-id/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_detail_wrong_method_post(self):
        """Use wrong http method post on detail"""
        response = self.client.post(self.detail_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_event_create_success(self):
        """Successfully create event"""
        data = {
            "title": "New Event",
            "description": "Event description",
            "start_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "end_at": (timezone.now() + timedelta(days=2, hours=3)).isoformat(),
            "capacity": 100,
            "status": "draft",
            "organizer": self.user.id,
            "community": self.community.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Event")

    def test_event_create_without_auth(self):
        """Create event without authentication"""
        self.client.force_authenticate(user=None)
        data = {"title": "New Event"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_create_missing_title(self):
        """Create event without title"""
        data = {
            "description": "Event description",
            "start_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "end_at": (timezone.now() + timedelta(days=2, hours=3)).isoformat(),
            "community": self.community.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_invalid_dates(self):
        """Create event with end date before start date"""
        data = {
            "title": "Invalid Event",
            "start_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "end_at": (timezone.now() + timedelta(days=1)).isoformat(), # End before start
            "community": self.community.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_update_success(self):
        """Successfully update event"""
        data = {"title": "Updated Title"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")

    def test_event_update_not_found(self):
        """Update event with non-existent id"""
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_update_without_auth(self):
        """Update event without authentication"""
        self.client.force_authenticate(user=None)
        data = {"title": "Updated Title"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_update_forbidden(self):
        """Update event as non-organizer"""
        self.client.force_authenticate(user=self.other_user)
        data = {"title": "Updated Title"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_delete_success(self):
        """Successfully delete event"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_event_delete_not_found(self):
        """Delete event with non-existent id"""
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_delete_without_auth(self):
        """Delete event without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_delete_forbidden(self):
        """Delete event as non-organizer"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)