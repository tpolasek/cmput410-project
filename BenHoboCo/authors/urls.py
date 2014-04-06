from django.conf.urls import url, patterns
from images.views import create_image
from .views import get_all_authors, get_author, get_author_images
from friends.views import add_friend, delete_friend, get_author_friends

urlpatterns = patterns('',
    #authors/author_name/friends - Specific Author Friends
    #authors/author_name/friends/friend_name - Specific Authors specific Friend
    url(r'^$', get_all_authors, name="authors"),
    url(r'^(?P<author_guid>[-\w]+)/$',get_author, name="author"),
    url(r'^(?P<author_guid>[-\w]+)/friends/addFriend/$', add_friend, name="author_add_friend"),
    url(r'^(?P<author_guid>[-\w]+)/friends/(?P<friend_guid>\w+)/delete/$', delete_friend, name="authors_delete_friend"),
    url(r'^(?P<author_guid>[-\w]+)/friends/$',get_author_friends, name="authors_specific_friend"),
    url(r'^(?P<author_guid>[-\w]+)/friends/(?P<friend_guid>\w+)/$',get_author_friends, name="authors_specific_friend"),

    url(r'^(?P<author_guid>[-\w]+)/images/create',create_image, name="create_image"),
    url(r'^(?P<author_guid>[-\w]+)/images/$',get_author_images, name="author_images"),
    url(r'^(?P<author_guid>[-\w]+)/images/(?P<image_id>\d+)/$',get_author_images, name="authors_specific_image"),
)