from django.conf.urls import url, patterns
from .views import posts, create_post, add_comment, delete_post
from authors.views import get_author_posts

urlpatterns = patterns('',
    url(r'^$', posts, name="posts"),
    url(r'^create/$', create_post, name="create_post"),
    url(r'^(?P<post_id>\d+)/$', posts, name="posts"),
    url(r'^(?P<post_id>\d+)/comment/$', add_comment, name="posts"),
    url(r'^(?P<post_id>\d+)/delete/$', delete_post, name="posts"),
    url(r'^author/(?P<author_guid>[-\w]+)/$', get_author_posts, name="author_posts"),
)