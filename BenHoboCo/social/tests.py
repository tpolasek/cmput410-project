from django.test import TestCase

from django.contrib.auth.models import User
from social.models import Author, Friend, Image, Post

from datetime import datetime

class TestCases(TestCase):
    def setUp(self):

    	user = User(username="test")
    	user.save()
    	author = Author(user=user)
    	author.save()

    	friend = Friend(name="friend", location="location", author = author)
    	friend.save()

    	image = Image(url='url', accessibility='private', author=author)
    	image.save()

    	post = Post(author=author, accessibility='public', content='content', time_stamp=datetime.now())
    	post.save()


    def test_author(self):
    	user = User.objects.get(username="test")
    	author = Author.objects.get(user=user)
    	self.assertEqual(author.user.username, 'test')

    def test_friend(self):
    	user = User.objects.get(username="test")
    	author = Author.objects.get(user=user)

    	friend = Friend.objects.get(name='friend', author=author)
    	self.assertEqual(friend.name, 'friend')
    	self.assertEqual(friend.location, 'location')

    def test_image(self):
    	user = User.objects.get(username="test")
    	author = Author.objects.get(user=user)

    	image = Image.objects.get(author=author)
    	self.assertEqual(image.url, 'url')
    	self.assertEqual(image.accessibility, 'private')

    def test_post(self):
    	user = User.objects.get(username="test")
    	author = Author.objects.get(user=user)

    	post = Post.objects.get(author=author)
    	self.assertEqual(post.accessibility, 'public')
    	self.assertEqual(post.content, 'content')