from django.contrib import admin
from solo.admin import SingletonModelAdmin
from social.models import *

# Register your models here.
admin.site.register(Author)
admin.site.register(Friend)
admin.site.register(Image)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SiteConfiguration, SingletonModelAdmin)

