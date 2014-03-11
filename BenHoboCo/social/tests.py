from django.test import TestCase
from django.test import Client
from social.models import *

# Create your tests here.
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
        self.assertEqual( len( Post.objects.all() ), 0 )
