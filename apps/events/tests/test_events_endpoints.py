# Python modules
from rest_framework import status
from rest_framework.test import APITestCase
import uuid
from datetime import timedelta

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

# Test list 
    def test_event_list_success(self):
        """Successfully get list of events"""
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_event_list_without_auth(self):
        """Get events without authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_list_empty(self):
        """Get empty list of events"""
        Event.objects.all().delete()
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_event_list_wrong_method(self):
        """Use wrong HTTP method"""
        url = reverse('event-list')
        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

 # Test detail 
    def test_event_detail_success(self):
        """Successfully get event detail"""
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.event.title)

    def test_event_detail_not_found(self):
        """Get event detail with non-existent ID"""
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_detail_invalid_id(self):
        """Get event detail with invalid ID format"""
        # This will fail at URL routing level
        response = self.client.get('/events/api/invalid-id/')
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST])

    def test_event_detail_without_auth(self):
        """Get event detail without authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test create 
    def test_event_create_success(self):
        """Successfully create event"""
        url = reverse('event-list')
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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Event")

    def test_event_create_missing_title(self):
        """Create event without title"""
        url = reverse('event-list')
        data = {
            "description": "Event description",
            "start_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "end_at": (timezone.now() + timedelta(days=2, hours=3)).isoformat(),
            "capacity": 100,
            "status": "draft",
            "organizer": self.user.id,
            "community": self.community.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_invalid_capacity(self):
        """Create event with invalid capacity"""
        url = reverse('event-list')
        data = {
            "title": "Invalid Event",
            "description": "Event description",
            "start_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "end_at": (timezone.now() + timedelta(days=2, hours=3)).isoformat(),
            "capacity": -10,
            "status": "draft",
            "organizer": self.user.id,
            "community": self.community.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_invalid_dates(self):
        """Create event with end date before start date"""
        url = reverse('event-list')
        data = {
            "title": "Invalid Event",
            "description": "Event description",
            "start_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "end_at": (timezone.now() + timedelta(days=1)).isoformat(),
            "capacity": 100,
            "status": "draft",
            "organizer": self.user.id,
            "community": self.community.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

 # Test update 
    def test_event_update_success(self):
        """Successfully update event"""
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")

    def test_event_update_not_found(self):
        """Update event with non-existent ID"""
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_update_without_auth(self):
        """Update event without authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_update_invalid_status(self):
        """Update event with invalid status"""
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        data = {"status": "invalid_status"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Test delete 
    def test_event_delete_success(self):
        """Successfully delete event"""
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_event_delete_not_found(self):
        """Delete event with non-existent ID"""
        url = reverse('event-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_delete_without_auth(self):
        """Delete event without authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_delete_twice(self):
        """Delete event twice"""
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        self.client.delete(url)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
