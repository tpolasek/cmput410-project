from django.conf.urls import patterns, url
from social import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^authors/$', views.get_all_authors, name="authors"),
    url(r'^authors/(?P<author_name>[-\w]+)/$',views.get_author, name="author"),
    url(r'^authors/(?P<author_name>[-\w]+)/posts/$',views.get_author_posts, name="author_posts"),
    url(r'^authors/(?P<author_name>[-\w]+)/posts/(?P<post_id>\w+)/$',views.get_author_posts, name="authors_specific_post"),
)