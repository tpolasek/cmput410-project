from django.conf.urls import patterns, url
from authors.views import user_update_author
from .views import index, user_logout, user_login, user_register
from .views import user_change_password, manage_account, upload_profile_image

urlpatterns = patterns('',

    url(r'^$', index, name="index"),

    #Authentication stuff
    url(r'^register/$', user_register, name="register"),
    url(r'^login/$', user_login, name="login"),
    url(r'^logout/$', user_logout, name="logout"),
    url(r'^manageAccount/updateAuthor/$', user_update_author, name="update_author"),
    url(r'^manageAccount/changePassword/$', user_change_password, name="change_password"),
    url(r'^manageAccount/$', manage_account, name="manage_account"),
    url(r'^manageAccount/changeImage/$', upload_profile_image, name="change_profile_picture"),
)