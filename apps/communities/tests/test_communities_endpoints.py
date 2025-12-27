# DRF
from rest_framework.test import APIClient
from rest_framework import status

# Python modules
from uuid import uuid4

# Django modules
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
        """Successfully get the list of communities"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_communities_without_auth(self):
        """Get communities without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_communities_wrong_method_put(self):
        """Use wrong http method put"""
        response = self.client.put(self.list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_communities_wrong_method_delete(self):
        """Use wrong http method delete on list endpoint"""
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_community_success(self):
        """Successfully create community"""
        data = {
            'name': 'New Community',
            'description': 'Test description',
            'visibility': 'public'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Community')

    def test_create_community_without_auth(self):
        """Create community without auth"""
        self.client.force_authenticate(user=None)
        data = {
            'name': 'New Community',
            'description': 'Test description'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_community_missing_name(self):
        """Create community without a name"""
        data = {
            'description': 'New community description'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_community_invalid_visibility(self):
        """Create community with wrong visibility"""
        data = {
            'name': 'New Community',
            'description': 'Test description',
            'visibility': 'invalid_visibility'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_community_detail_success(self):
        """Successfully get community detail"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Community')

    def test_community_detail_not_found(self):
        """Get community detail with not existing id"""
        invalid_url = f'/communities/api/{uuid4()}/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_community_detail_invalid_id(self):
        """Get community detail with wrong id format"""
        invalid_url = '/communities/api/invalid-id/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_community_detail_wrong_method(self):
        """Use wrong http method post on detail endpoint"""
        response = self.client.post(self.detail_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_community_success(self):
        """Successfully update community"""
        data = {'name': 'Updated Community'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Community')

    def test_update_community_without_auth(self):
        """Update community without auth"""
        self.client.force_authenticate(user=None)
        data = {'name': 'Updated Community'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_community_not_found(self):
        """Update community with not existenting id"""
        invalid_url = f'/communities/api/{uuid4()}/'
        data = {'name': 'Updated Community'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_community_invalid_data(self):
        """Update community with invalid data"""
        data = {'name': ''}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_community_success(self):
        """Successfully delete community"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Community.objects.filter(id=self.community.id).exists())

    def test_delete_community_without_auth(self):
        """Delete community without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_community_not_found(self):
        """Delete community with non-existent id"""
        invalid_url = f'/communities/api/{uuid4()}/'
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_community_forbidden(self):
        """Delete community as non owner"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewset_list_communities_success(self):
        """Successfully get list via viewset"""
        response = self.client.get(self.viewset_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_viewset_create_community_success(self):
        """Successfully create community via viewset"""
        data = {
            'name': 'New Community ViewSet',
            'description': 'New community description',
            'visibility': 'public'
        }
        response = self.client.post(self.viewset_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Community ViewSet')

    def test_viewset_create_community_without_auth(self):
        """Create community via viewset without authentication"""
        self.client.force_authenticate(user=None)
        data = {
            'name': 'New Community',
            'description': 'New community description'
        }
        response = self.client.post(self.viewset_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_viewset_create_community_invalid_data(self):
        """Create community via viewset with invalid data"""
        data = {
            'name': '',
            'description': 'New community description'
        }
        response = self.client.post(self.viewset_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_viewset_create_community_invalid_visibility(self):
        """Create community via viewset with invalid visibility"""
        data = {
            'name': 'New Community',
            'visibility': 'unknown'
        }
        response = self.client.post(self.viewset_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_viewset_update_community_success(self):
        """Successfully update community through viewset"""
        data = {'name': 'Updated via ViewSet'}
        response = self.client.patch(self.viewset_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated via ViewSet')

    def test_viewset_update_community_not_found(self):
        """Update community via viewset with not existing id"""
        invalid_url = f'/communities/{uuid4()}/'
        data = {'name': 'Updated'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_viewset_update_community_without_auth(self):
        """Update community via viewset without auth"""
        self.client.force_authenticate(user=None)
        data = {'name': 'Updated'}
        response = self.client.patch(self.viewset_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_viewset_update_community_invalid_data(self):
        """Update community via viewset with invalid data"""
        data = {'name': ''}
        response = self.client.patch(self.viewset_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_viewset_delete_community_success(self):
        """Successfully delete community through viewset"""
        response = self.client.delete(self.viewset_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_viewset_delete_community_not_found(self):
        """Delete community via viewset with not existing id"""
        invalid_url = f'/communities/{uuid4()}/'
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_viewset_delete_community_without_auth(self):
        """Delete community via viewset without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.viewset_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_viewset_delete_community_forbidden(self):
        """Delete community via viewset as non owner"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.viewset_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)