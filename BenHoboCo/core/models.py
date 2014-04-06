from django.db import models
from solo.models import SingletonModel

ACCESSIBILITY_TYPES = (
    ('PUBLIC', 'Public'),
    ('PRIVATE', 'Private'),
    ('private_to_another', 'Private To another author'),
    ('SERVERONLY', 'Friends on this host'),
    ('FRIENDS', 'Friends'),
    ('FOAF', 'Friends of friends'),
)

class SiteConfiguration(SingletonModel):
    #Share posts on other servers (global flag)
    share_posts_remote = models.BooleanField(default=True)

    #Require the server admin to OKAY new users
    manual_user_signup = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"