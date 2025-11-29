# Python modules
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4

# Django modules
from django.urls import reverse
from django.test import TestCase

# Project modules
from apps.users.models import CustomUser
from apps.posts.models import Post, Tag


class PostEnpointsTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            email = 'testuser@example.com',
            username = 'testuser',
            full_name = 'Test User',
            password = '12345'
        )
        self.client.force_authenticate(user=self.user)

        self.tag = Tag.objects.create(name='TestTag')

        self.post = Post.objects.create(
            author = self.user,
            content = "Its a test post"
        )
        self.post.tags.add(self.tag)

        self.list_url = "/posts/api/"
        self.detail_url = f"/posts/api/{self.post.id}/"

# List of posts tags 
    def test_list_posts_success(self):
        """successfully get list of posts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_posts_without_auth(self):
        """not authentificated"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_posts_empty(self):
        """No posts in database"""
        Post.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_posts_wrong_method(self):
        """metgod POST instead of GET"""
        response = self.client.get(self.list_url, {})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

# Post creation tests
    def test_create_post_success(self):
        """successfully create post"""
        data = {'author': self.user.id, 'content': 'New post'}
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'New post')

    def test_create_post_without_auth(self):
        """not authentificated"""
        self.client.force_authenticate(user=None)
        data = {'author': self.user.id, 'content': 'New post'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post_empty_content(self):
        """missing content"""
        data = {'author': self.user.id, 'content': ''}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)

    def test_create_post_invalid_author(self):
        """wrong author id"""
        data = {'author': uuid4(), 'content':'New post'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Posts detail and update tests
    def test_update_post_success(self):
        """partially update successfully"""
        data = {'content': 'Updated post'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content', 'Updated post'])

    def test_update_post_without_auth(self):
        """not authenticated"""
        self.client.force_authenticate(user=None)
        data = {'content': 'Updated post'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_invalid_id(self):
        """not existent post id"""
        invalid_url = f'/posts/api/{uuid4()}/'
        data = {'content': 'Updated post'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_empty_content(self):
        """empty content"""
        data = {'content': ''}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Posts delete tests
    def test_delete_post_success(self):
        """successfully delete post"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_without_auth(self):
        """not authenticated"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_invalid_id(self):
        """wrong post id (doesnt exist)"""
        invalid_url = f'/posts/api/{uuid4()}/'
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_twice(self):
        """delete the same post two times"""
        self.client.delete(self.detail_url)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
