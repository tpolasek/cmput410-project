from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BenHoboCo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('core.urls')),
    url(r'^api/',include('api.urls')),
    url(r'^authors/',include('authors.urls')),
    url(r'^images/',include('images.urls')),
    url(r'^posts/',include('posts.urls')),
    url(r'^friends/',include('friends.urls')),
)

if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
