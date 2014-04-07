from django.conf.urls import url, patterns
from .views import posts, create_post, add_comment, delete_post
from authors.views import get_author_posts
from .views import CreatePost

urlpatterns = patterns('',
    url(r'^$', posts, name="posts"),
    url(r'^(?P<post_id>\d+)/$', posts, name="posts"),
    url(regex=r'^(?P<post_id>\d+)/comment/$', view=add_comment, name="add_comment"),
    url(r'^(?P<post_id>\d+)/delete/$', delete_post, name="delete_comment"),
    url(r'^author/(?P<author_guid>\d+)/$', get_author_posts, name="author_posts"),

    url(
        regex = r'^create/$',
        view = CreatePost.as_view(),
        name = "create_post"
    ),
)