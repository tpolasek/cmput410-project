from django.conf.urls import url, patterns
from .views import friends, search_friend

urlpatterns = patterns('',
    # Friends
    url(r'^$',friends, name="author_friends"),
    url(r'^search/$',search_friend, name="authors_search_friend"),
)