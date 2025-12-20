# Python modules
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4

# Django modules
from django.urls import reverse
from django.test import TestCase

# Project modules
from apps.users.models import CustomUser
from apps.posts.models import Post, Tag, Comment, Like
from apps.communities.models import Community


class PostEndpointsTests(TestCase):
    """Tests for post endpoints"""
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
            owner=self.user
        )

        self.tag = Tag.objects.create(name='TestTag')

        self.post = Post.objects.create(
            author=self.user,
            content="It's a test post",
            community=self.community
        )
        self.post.tags.add(self.tag)

        self.list_url = "/posts/api/"
        self.detail_url = f"/posts/api/{self.post.id}/"
        self.v1_list_url = "/posts/v1/"
        self.v1_detail_url = f"/posts/v1/{self.post.id}/"
        self.comments_url = f"/posts/{self.post.id}/comments/"
        self.like_url = f"/posts/{self.post.id}/like/"

# List posts
    def test_list_posts_success(self):
        """Successfully get list of posts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_posts_without_auth(self):
        """Get posts without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_posts_empty(self):
        """No posts in database"""
        Post.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_posts_with_community_filter(self):
        """Get posts filtered by community"""
        response = self.client.get(self.list_url, {'community': str(self.community.id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Post creation 
    def test_create_post_success(self):
        """Successfully create post"""
        data = {'content': 'New post content'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'New post content')

    def test_create_post_without_auth(self):
        """Create post without authentication"""
        self.client.force_authenticate(user=None)
        data = {'content': 'New post'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post_empty_content(self):
        """Create post with empty content"""
        data = {'content': ''}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)

    def test_create_post_missing_content(self):
        """Create post without content field"""
        data = {}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)

# Post detail 
    def test_post_detail_success(self):
        """Successfully get post detail"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "It's a test post")

    def test_post_detail_not_found(self):
        """Get post detail with non-existent ID"""
        invalid_url = f'/posts/api/{uuid4()}/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_detail_invalid_id(self):
        """Get post detail with invalid ID format"""
        invalid_url = '/posts/api/invalid-id/'
        response = self.client.get(invalid_url)
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST])

    def test_post_detail_without_auth(self):
        """Get post detail without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Post update 
    def test_update_post_success(self):
        """Partially update post successfully"""
        data = {'content': 'Updated post content'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated post content')

    def test_update_post_without_auth(self):
        """Update post without authentication"""
        self.client.force_authenticate(user=None)
        data = {'content': 'Updated post'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_invalid_id(self):
        """Update post with non-existent ID"""
        invalid_url = f'/posts/api/{uuid4()}/'
        data = {'content': 'Updated post'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_empty_content(self):
        """Update post with empty content"""
        data = {'content': ''}
        response = self.client.patch(self.detail_url, data, format='json')
        # Empty content might be allowed for partial update
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

# Post delete 
    def test_delete_post_success(self):
        """Successfully delete post"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id, deleted_at__isnull=True).exists())

    def test_delete_post_without_auth(self):
        """Delete post without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_invalid_id(self):
        """Delete post with non-existent ID"""
        invalid_url = f'/posts/api/{uuid4()}/'
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_twice(self):
        """Delete the same post twice"""
        self.client.delete(self.detail_url)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# ViewSet list 
    def test_v1_list_posts_success(self):
        """Successfully get list of posts via ViewSet"""
        response = self.client.get(self.v1_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_v1_list_posts_without_auth(self):
        """Get posts via ViewSet without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.v1_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_v1_list_posts_empty(self):
        """Get empty list via ViewSet"""
        Post.objects.all().delete()
        response = self.client.get(self.v1_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_v1_list_posts_wrong_method(self):
        """Use wrong HTTP method"""
        response = self.client.put(self.v1_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

# ViewSet create 
    def test_v1_create_post_success(self):
        """Successfully create post via ViewSet"""
        data = {'content': 'New post via ViewSet'}
        response = self.client.post(self.v1_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'New post via ViewSet')

    def test_v1_create_post_without_auth(self):
        """Create post via ViewSet without authentication"""
        self.client.force_authenticate(user=None)
        data = {'content': 'New post'}
        response = self.client.post(self.v1_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_v1_create_post_empty_content(self):
        """Create post via ViewSet with empty content"""
        data = {'content': ''}
        response = self.client.post(self.v1_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_v1_create_post_missing_content(self):
        """Create post via ViewSet without content"""
        data = {}
        response = self.client.post(self.v1_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

 # ViewSet update 
    def test_v1_update_post_success(self):
        """Successfully update post via ViewSet"""
        data = {'content': 'Updated via ViewSet'}
        response = self.client.patch(self.v1_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated via ViewSet')

    def test_v1_update_post_without_auth(self):
        """Update post via ViewSet without authentication"""
        self.client.force_authenticate(user=None)
        data = {'content': 'Updated'}
        response = self.client.patch(self.v1_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_v1_update_post_invalid_id(self):
        """Update post via ViewSet with invalid ID"""
        invalid_url = f'/posts/v1/{uuid4()}/'
        data = {'content': 'Updated'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_v1_update_post_invalid_data(self):
        """Update post via ViewSet with invalid data"""
        data = {'invalid_field': 'value'}
        response = self.client.patch(self.v1_detail_url, data, format='json')
        # Should still succeed for partial update
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

 # ViewSet delete 
    def test_v1_delete_post_success(self):
        """Successfully delete post via ViewSet"""
        response = self.client.delete(self.v1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_v1_delete_post_without_auth(self):
        """Delete post via ViewSet without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.v1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_v1_delete_post_invalid_id(self):
        """Delete post via ViewSet with invalid ID"""
        invalid_url = f'/posts/v1/{uuid4()}/'
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_v1_delete_post_twice(self):
        """Delete post via ViewSet twice"""
        self.client.delete(self.v1_detail_url)
        response = self.client.delete(self.v1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# User posts 
    def test_get_user_posts_success(self):
        """Successfully get posts by user"""
        url = f'/posts/v1/user/{self.user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_user_posts_invalid_user(self):
        """Get posts for non-existent user"""
        url = f'/posts/v1/user/{uuid4()}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_posts_without_auth(self):
        """Get user posts without authentication"""
        self.client.force_authenticate(user=None)
        url = f'/posts/v1/user/{self.user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_posts_empty(self):
        """Get posts for user with no posts"""
        Post.objects.filter(author=self.other_user).delete()
        url = f'/posts/v1/user/{self.other_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

# Comments 
    def test_list_comments_success(self):
        """Successfully get list of comments"""
        Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Test comment"
        )
        response = self.client.get(self.comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_list_comments_post_not_found(self):
        """Get comments for non-existent post"""
        invalid_url = f'/posts/{uuid4()}/comments/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_comments_empty(self):
        """Get comments when no comments exist"""
        Comment.objects.filter(post=self.post).delete()
        response = self.client.get(self.comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_comment_success(self):
        """Successfully create comment"""
        data = {'content': 'New comment'}
        response = self.client.post(self.comments_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'New comment')

    def test_create_comment_without_auth(self):
        """Create comment without authentication"""
        self.client.force_authenticate(user=None)
        data = {'content': 'New comment'}
        response = self.client.post(self.comments_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_empty_content(self):
        """Create comment with empty content"""
        data = {'content': ''}
        response = self.client.post(self.comments_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_post_not_found(self):
        """Create comment for non-existent post"""
        invalid_url = f'/posts/{uuid4()}/comments/'
        data = {'content': 'New comment'}
        response = self.client.post(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# Like
    def test_like_post_success(self):
        """Successfully like a post"""
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.user).exists())

    def test_like_post_without_auth(self):
        """Like post without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_post_already_liked(self):
        """Like post that is already liked"""
        Like.objects.create(post=self.post, user=self.user)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_post_not_found(self):
        """Like non-existent post"""
        invalid_url = f'/posts/{uuid4()}/like/'
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unlike_post_success(self):
        """Successfully unlike a post"""
        Like.objects.create(post=self.post, user=self.user)
        response = self.client.delete(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(post=self.post, user=self.user).exists())

    def test_unlike_post_without_auth(self):
        """Unlike post without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unlike_post_not_liked(self):
        """Unlike post that is not liked"""
        response = self.client.delete(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unlike_post_not_found(self):
        """Unlike non-existent post"""
        invalid_url = f'/posts/{uuid4()}/like/'
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
