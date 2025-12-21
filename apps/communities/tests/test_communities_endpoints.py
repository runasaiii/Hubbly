# Python modules
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4

# Django modules
from django.urls import reverse
from django.test import TestCase

# Project modules
from apps.users.models import CustomUser
from apps.communities.models import Community


class CommunityEndpointsTests(TestCase):
    """Tests for community endpoints"""
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

        self.community = Community.objects.create(
            name='Test Community',
            description='Test description',
            owner=self.user
        )

        self.list_url = '/communities/api/'
        self.detail_url = f'/communities/api/{self.community.id}/'
        self.viewset_list_url = '/communities/'
        self.viewset_detail_url = f'/communities/{self.community.id}/'


    def test_list_communities_success(self):
        """successfully get the list of communities"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_communities_without_auth(self):
        """get communities without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_communities_empty(self):
        """get empty list of communities"""
        Community.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_communities_wrong_method(self):
        """use wrong http method"""
        response = self.client.put(self.list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_create_community_success(self):
        """successfully create community"""
        data = {
            'name': 'New Community',
            'description': 'Test description',
            'visibility': 'public'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Community')

    def test_create_community_without_auth(self):
        """create community without auth"""
        self.client.force_authenticate(user=None)
        data = {
            'name': 'New Community',
            'description': 'Test description'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_community_missing_name(self):
        """create community withouta name"""
        data = {
            'description': 'New community description'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_community_invalid_visibility(self):
        """create community with wrong visibility"""
        data = {
            'name': 'New Community',
            'description': 'Test description',
            'visibility': 'invalid_visibility'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_community_detail_success(self):
        """successfully get community detail"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Community')

    def test_community_detail_not_found(self):
        """get community detail with not existing ID"""
        invalid_url = f'/communities/api/{uuid4()}/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_community_detail_invalid_id(self):
        """get community detail with wrong ID format"""
        invalid_url = '/communities/api/invalid-id/'
        response = self.client.get(invalid_url)
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST])

    def test_community_detail_without_auth(self):
        """get community detail without auth"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_community_success(self):
        """successfully update community"""
        data = {'name': 'Updated Community'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Community')

    def test_update_community_without_auth(self):
        """Update community without auth"""
        self.client.force_authenticate(user=None)
        data = {'name': 'Updated Community'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_community_not_found(self):
        """Update community with not existenting ID"""
        invalid_url = f'/communities/api/{uuid4()}/'
        data = {'name': 'Updated Community'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_community_invalid_visibility(self):
        """Update community with wrong visibility"""
        data = {'visibility': 'invalid_visibility'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_delete_community_success(self):
        """Successfully delete community"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Community.objects.filter(id=self.community.id, deleted_at__isnull=True).exists())

    def test_delete_community_without_auth(self):
        """Delete community without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_community_not_found(self):
        """Delete community with non-existent ID"""
        invalid_url = f'/communities/api/{uuid4()}/'
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_community_twice(self):
        """Delete community twice"""
        self.client.delete(self.detail_url)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_viewset_list_communities_success(self):
        """Successfully get list via ViewSet"""
        response = self.client.get(self.viewset_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_viewset_list_communities_without_auth(self):
        """Get communities via ViewSet without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.viewset_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewset_list_communities_empty(self):
        """Get empty list via ViewSet"""
        Community.objects.all().delete()
        response = self.client.get(self.viewset_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_viewset_list_communities_wrong_method(self):
        """Use wrong HTTP method"""
        response = self.client.put(self.viewset_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_viewset_create_community_success(self):
        """Successfully create community via ViewSet"""
        data = {
            'name': 'New Community ViewSet',
            'description': 'New community description',
            'visibility': 'public'
        }
        response = self.client.post(self.viewset_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Community ViewSet')

    def test_viewset_create_community_without_auth(self):
        """Create community via ViewSet without authentication"""
        self.client.force_authenticate(user=None)
        data = {
            'name': 'New Community',
            'description': 'New community description'
        }
        response = self.client.post(self.viewset_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_viewset_create_community_missing_name(self):
        """Create community via ViewSet without name"""
        data = {
            'description': 'New community description'
        }
        response = self.client.post(self.viewset_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_viewset_create_community_invalid_data(self):
        """Create community via ViewSet with invalid data"""
        data = {
            'name': '',
            'description': 'New community description'
        }
        response = self.client.post(self.viewset_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_viewset_update_community_success(self):
        """Successfully update community through ViewSet"""
        data = {'name': 'Updated via ViewSet'}
        response = self.client.patch(self.viewset_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated via ViewSet')

    def test_viewset_update_community_not_found(self):
        """Update community via ViewSet with not existing ID"""
        invalid_url = f'/communities/{uuid4()}/'
        data = {'name': 'Updated'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_viewset_update_community_without_auth(self):
        """Update community via ViewSet without auth"""
        self.client.force_authenticate(user=None)
        data = {'name': 'Updated'}
        response = self.client.patch(self.viewset_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_viewset_update_community_invalid_data(self):
        """Update community via ViewSet with wrong data"""
        data = {'visibility': 'invalid'}
        response = self.client.patch(self.viewset_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_viewset_delete_community_success(self):
        """Successfully delete community through ViewSet"""
        response = self.client.delete(self.viewset_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_viewset_delete_community_not_found(self):
        """Delete community via ViewSet with not existing ID"""
        invalid_url = f'/communities/{uuid4()}/'
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_viewset_delete_community_without_auth(self):
        """Delete community via ViewSet without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.viewset_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_viewset_delete_community_twice(self):
        """Delete community via ViewSet twice"""
        self.client.delete(self.viewset_detail_url)
        response = self.client.delete(self.viewset_detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



