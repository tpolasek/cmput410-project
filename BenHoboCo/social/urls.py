from django.conf.urls import patterns, url
from social import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),

    #Authentication stuff
    url(r'^register/$', views.user_register),
    url(r'^login/$', views.user_login),
    url(r'^logout/$', views.user_logout),


    #authors - All Authors
    #authors/author_name/ - Specific Author

    #authors/author_name/friends - Specific Author Friends
    #authors/author_name/friends/friend_name - Specific Authors specific Friend
    url(r'^authors/$', views.get_all_authors, name="authors"),
    url(r'^authors/(?P<author_name>[-\w]+)/$',views.get_author, name="author"),
    url(r'^authors/(?P<author_name>[-\w]+)/friends/$',views.get_author_friends, name="author_friends"),
    url(r'^authors/(?P<author_name>[-\w]+)/friends/addfriend/$', views.add_remote_friend, name="author_add_friend"),
    url(r'^authors/(?P<author_name>[-\w]+)/friends/(?P<friend_name>\w+)/delete/$',views.delete_friend, name="authors_delete_friend"),
    url(r'^authors/(?P<author_name>[-\w]+)/friends/(?P<friend_name>\w+)/$',views.get_author_friends, name="authors_specific_friend"),

    #This should be changed to
    #images/author/author_name
    #images/author/author_name/image_id or #images/image_id
    url(r'^authors/(?P<author_name>[-\w]+)/images/$',views.get_author_images, name="author_images"),
    url(r'^authors/(?P<author_name>[-\w]+)/images/(?P<image_id>\d+)/$',views.get_author_images, name="authors_specific_image"),    

    #posts - all posts
    #posts/post_id - specific post
    #posts/author/bensontrinh - specific posts from a person
    url(r'^posts/$', views.posts, name="posts"),
    url(r'^posts/(?P<post_id>\d+)/$', views.posts, name="posts"),
    url(r'^posts/create/$', views.create_post, name="create_post"),
    url(r'^posts/(?P<post_id>\d+)/delete/$', views.delete_post, name="posts"),

    url(r'^posts/author/(?P<author_name>[-\w]+)/$', views.get_author_posts, name="author_posts"),

    url(r'^authors/(?P<author_name>[-\w]+)/images/upload/$', views.upload_image, name="upload_image"),

    #REMOVE THE FOLLOWING LATER
    url(r'^authors/(?P<author_name>[-\w]+)/posts/$',views.get_author_posts, name="author_posts"),
    url(r'^authors/(?P<author_name>[-\w]+)/posts/(?P<post_id>\w+)/$',views.get_author_posts, name="authors_specific_post"),
)