from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField

# Create your models here.
class Author(models.Model):

    #User already contains: username, password, first_name, last_name, email
    user = models.OneToOneField(User)

    image = models.ImageField( null = True, blank=True, upload_to="Images")
    host = models.URLField(max_length=256) #This specifies the authors host

    guid = UUIDField()

    github = models.CharField(max_length=30, default="")

    url = models.URLField(max_length=256) #This specifies the url of the authors page

    def __unicode__(self):
        return self.user.username

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return ""

    def get_full_name(self):
        return "%s %s" % ( self.user.first_name, self.user.last_name )

    def json(self):
        return dict (
            id = self.guid,
            host = self.host,
            displayname = self.get_full_name(),
            url = "%s/authors/%s" % (self.host, self.guid),
            github = self.github
        )