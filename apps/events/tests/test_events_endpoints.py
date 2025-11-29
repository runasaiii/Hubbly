# Python modules
from rest_framework import status
from rest_framework.test import APITestCase
import uuid

# Django modules
from django.urls import reverse
from django.utils import timezone

# Project modules
from apps.users.models import CustomUser
from apps.communities.models import Community
from apps.events.models import Event


class EventAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            full_name="Test User",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.community = Community.objects.create(
            name="Test Community",
            slug="test-community"
        )

        self.event = Event.objects.create(
            title="Sample Event",
            description="This is a sample event.",
            start_at=timezone.now(),
            end_at=timezone.now() + timezone.timedelta(hours=2),
            capacity=50,
            status="draft",
            organizer=self.user,
            community=self.community,
        )

# Test list endpoint
    def test_event_list_success(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


# Test detail endpoint
    def test_event_detail_success(self):
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.event.title)

    def test_event_detail_not_found(self):
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Test create endpoint
    def test_event_create_success(self):
        url = reverse('event-list')
        data = {
            "title": "New Event",
            "description": "Event description",
            "start_at": timezone.now(),
            "end_at": timezone.now() + timezone.timedelta(hours=3),
            "capacity": 100,
            "status": "draft",
            "organizer": self.user.id,
            "community": self.community.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Event")

    def test_event_create_missing_title(self):
        url = reverse('event-list')
        data = {
            "description": "Event description",
            "start_at": timezone.now(),
            "end_at": timezone.now() + timezone.timedelta(hours=3),
            "capacity": 100,
            "status": "draft",
            "organizer": self.user.id,
            "community": self.community.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_invalid_capacity(self):
        url = reverse('event-list')
        data = {
            "title": "Invalid Event",
            "description": "Event description",
            "start_at": timezone.now(),
            "end_at": timezone.now() + timezone.timedelta(hours=3),
            "capacity": -10,
            "status": "draft",
            "organizer": self.user.id,
            "community": self.community.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Test update endpoint
    def test_event_update_success(self):
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")

    def test_event_update_not_found(self):
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Test delete endpoint
    def test_event_delete_success(self):
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_event_delete_not_found(self):
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
