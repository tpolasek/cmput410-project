from django.conf.urls import url, patterns
from .views import friends, search_friend, accept_friend_request

urlpatterns = patterns('',
    # Friends
    url(r'^$',friends, name="author_friends"),
    url(r'^search/$',search_friend, name="authors_search_friend"),
    url(r'^acceptrequest/(?P<friend_id>[-\w]+)/',accept_friend_request, name="accept_friend_request"),
)