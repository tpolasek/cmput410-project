from django.conf.urls import url, patterns
from authors.views import get_author_images
from .views import create_image, upload_image

urlpatterns = patterns('',
    url(r'^$', get_author_images, name="author_images"),
    url(r'^(?P<image_id>\d+)/$', get_author_images, name="author_images"),
    url(r'^create/$', create_image, name="create_image"),
    url(r'^upload/$', upload_image,name="upload_images"),
)