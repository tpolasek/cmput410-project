from django.conf.urls import url, patterns
from .views import posts, create_post, add_comment, delete_post
from authors.views import get_author_posts
from .views import CreatePost

urlpatterns = patterns('',
    url(r'^$', posts, name="posts"),
    url(r'^(?P<post_id>[-\w]+)/$', posts, name="posts"),
    url(r'^(?P<post_id>[-\w]+)/comment/$', add_comment, name="posts"),
    url(r'^(?P<post_id>[-\w]+)/delete/$', delete_post, name="posts"),
    url(r'^author/(?P<author_guid>[-\w]+)/$', get_author_posts, name="author_posts"),

    url(
        regex = r'^create/$',
        view = CreatePost.as_view(),
        name = "create_post"
    ),
)