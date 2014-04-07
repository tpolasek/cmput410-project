from django.conf.urls import patterns, url, include

from .views import AuthorList, AuthorDetail
from .views import FriendList, FriendDetail, FriendCompare, FriendRequestView
from .views import ImageList, ImageDetail
from .views import PostList, AuthorPostList, PostDetail, PostsVisibileToAuthor

author_urls = patterns('',
    url(r'^$', AuthorList.as_view(), name="all_authors"),
    url(r'^(?P<guid>[-\w]+)/$', AuthorDetail.as_view(), name="specific_author"),
    url(r'^(?P<guid>[-\w]+)/posts/$', AuthorPostList.as_view(), name="specific_author_posts"),
)

post_urls = patterns('',
    url(r'^$', PostList.as_view(), name="posts" ),
    url(r'^(?P<guid>[-\w]+)/$', PostDetail.as_view(), name="post_detail"),
)

friends_urls = patterns('',
    url(r'^$',FriendList.as_view(), name="author_friends"),
    url(r'^(?P<guid_1>[-\w]+)/(?P<guid_2>[-\w]+)/$', FriendCompare.as_view(), name="compare_friends" ),
)

urlpatterns = patterns('',
    url(r'^authors/',include(author_urls)),
    url(r'^posts/',include(post_urls)),
    url(r'^my_posts/$', PostsVisibileToAuthor.as_view(), name="my_posts"),
    url(r'^friends/',include(friends_urls)),
    url(r'^friendrequest/$', FriendRequestView.as_view(), name="friendrequest")
)