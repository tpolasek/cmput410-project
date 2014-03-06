from django.conf.urls import patterns, url
from social import views

urlpatterns = patterns('',
    url(r'^$',views.authors, name="authors"),
)