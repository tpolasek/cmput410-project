from django.conf.urls import patterns, url
from social import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),

    url(r'^authors/$', views.get_all_authors, name="authors"),
    url(r'^authors/(?P<author_name>[-\w]+)/$',views.get_author, name="author"),

    url(r'^authors/(?P<author_name>[-\w]+)/posts/$',views.get_author_posts, name="author_posts"),
    url(r'^authors/(?P<author_name>[-\w]+)/posts/(?P<post_id>\w+)/$',views.get_author_posts, name="authors_specific_post"),
    url(r'^authors/(?P<author_name>[-\w]+)/post/$', views.create_post, name="author_create_post"),

    url(r'^authors/(?P<author_name>[-\w]+)/images/$',views.get_author_images, name="author_images"),
    url(r'^authors/(?P<author_name>[-\w]+)/images/(?P<image_id>\w+)/$',views.get_author_images, name="authors_specific_image"),
    url(r'^register/$', views.user_register),
    url(r'^login/$', views.user_login),
    url(r'^logout/$', views.user_logout),

    url(r'^authors/(?P<author_name>[-\w]+)/friends/$',views.get_author_friends, name="author_friends"),
    url(r'^authors/(?P<author_name>[-\w]+)/friends/(?P<friend_name>\w+)/$',views.get_author_friends, name="authors_specific_friend"),
)