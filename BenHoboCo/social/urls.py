from django.conf.urls import patterns, url
from social import views, api_views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),

    #Authentication stuff
    url(r'^register/$', views.user_register),
    url(r'^login/$', views.user_login),
    url(r'^logout/$', views.user_logout),
    url(r'^manageAccount/updateAuthor/$', views.user_update_author),
    url(r'^manageAccount/changePassword/$', views.user_change_password),
    url(r'^manageAccount/$', views.manage_account),
    url(r'^manageAccount/changeImage/$', views.upload_profile_image),

    #authors - All Authors
    #authors/author_name/ - Specific Author

    #authors/author_name/friends - Specific Author Friends
    #authors/author_name/friends/friend_name - Specific Authors specific Friend
    url(r'^authors/$', views.get_all_authors, name="authors"),
    url(r'^authors/(?P<author_guid>[-\w]+)/$',views.get_author, name="author"),
    url(r'^authors/(?P<author_guid>[-\w]+)/friends/addFriend/$', views.add_friend, name="author_add_friend"),
    url(r'^authors/(?P<author_guid>[-\w]+)/friends/(?P<friend_guid>\w+)/delete/$',views.delete_friend, name="authors_delete_friend"),
    url(r'^authors/(?P<author_guid>[-\w]+)/friends/$',views.get_author_friends, name="authors_specific_friend"),
    url(r'^authors/(?P<author_guid>[-\w]+)/friends/(?P<friend_guid>\w+)/$',views.get_author_friends, name="authors_specific_friend"),

    # Friends
    url(r'^friends/$',views.friends, name="author_friends"),
    url(r'^friends/search/$',views.search_friend, name="authors_search_friend"),

    #This should be changed to
    #images/author/author_name
    #images/author/author_name/image_id or #images/image_id
    url(r'^images/$',views.get_author_images, name="author_images"),
    url(r'^images/(?P<image_id>\d+)/$',views.get_author_images, name="author_images"),
    url(r'^images/create/$',views.create_image, name="create_image"),
    url(r'^images/upload/$', views.upload_image,name="upload_images"),
    url(r'^authors/(?P<author_guid>[-\w]+)/images/create',views.create_image, name="create_image"),
    url(r'^authors/(?P<author_guid>[-\w]+)/images/$',views.get_author_images, name="author_images"),
    url(r'^authors/(?P<author_guid>[-\w]+)/images/(?P<image_id>\d+)/$',views.get_author_images, name="authors_specific_image"),    

    #posts - all posts
    #posts/post_id - specific post
    #posts/author/bensontrinh - specific posts from a person
    url(r'^posts/$', views.posts, name="posts"),
    url(r'^posts/create/$', views.create_post, name="create_post"),
    url(r'^posts/(?P<post_id>\d+)/$', views.posts, name="posts"),
    url(r'^posts/(?P<post_id>\d+)/comment/$', views.add_comment, name="posts"),
    url(r'^posts/(?P<post_id>\d+)/delete/$', views.delete_post, name="posts"),
    url(r'^posts/author/(?P<author_guid>[-\w]+)/$', views.get_author_posts, name="author_posts"),


    #API
    url(r'^api/authors/$', api_views.get_authors, name="get_authors"),
    url(r'^api/authors/(?P<author_guid>[-\w]+)/$', api_views.get_authors, name="get_authors"),
    url(r'^api/authors/(?P<author_guid>[-\w]+)/posts/$', api_views.get_posts, name="api_get_posts"),
    url(r'^api/authors/(?P<author_guid>[-\w]+)/posts/(?P<post_guid>[-\w]+)/$', api_views.get_posts, name="api_get_posts"),

    #POST a list of friends and returns a list of friends who the <author_guid> is friends with
    #url(r'^api/friends/(?P<author_guid>[-\w]+)/$', api_views.get_friends, name="friends"),

    #Compares the two provided friends and checks if they are friends
    url(r'^api/friends/(?P<friend1_guid>[-\w]+)/(?P<friend2_guid>[-\w]+)/$', api_views.compare_friends, name="compare_friends"),
    
    #Friend request
    url(r'^api/friendrequest/$', api_views.friend_request, name="friend_request"),
)
