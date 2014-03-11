from django.test import TestCase
from django.test import Client
from social.models import *

from django.contrib.auth.models import User

from datetime import datetime
from markdown2 import markdown
class PostTestCase(TestCase):
    def setUp(self):
       global c
       c = Client()
       c.post('/register/', {'username':"test", 'password':'testing', 'first_name':"Test",'last_name':"User", "email":"test@test.com" })
       c.post('/login/', {'username':'test', 'password':'testing' })

    def test_create(self):
        response = c.post('/posts/create/', {'access':'public', 'content':'test_content','content_type':"text"})
        self.assertEqual( response.status_code, 302 )
        post = Post.objects.latest('id')
        self.assertEqual( post.content, '<pre>test_content</pre>')

    def test_get_all(self):
        response = c.get('/posts/')
        self.assertEqual( response.status_code, 200 )

    def test_delete(self):
        response = c.post('/posts/1/delete' )
        self.assertEqual( len( Post.objects.all()), 0 )

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

    def test_create_delete_post(self):
        user = User.objects.get(username="test")
        author = Author.objects.get(user=user)
        access = 'public'
	content = 'test'
        
	p = Post(author=author, accessibility=access, content=content)
        p.save()
	new_post_id = p.id
	self.assertNotEqual(p.id, 0)
	
	post = Post.objects.get(id=new_post_id)
        self.assertEqual(post.content,"test")
	post.delete()

    def test_markdown(self):
        self.assertEqual(markdown("*test*"),"<p><em>test</em></p>\n")
        self.assertEqual(markdown("**test**"),"<p><strong>test</strong></p>\n")
        self.assertEqual(markdown("[test](lol.com)"),"<p><a href=\"lol.com\">test</a></p>\n")
