from django.db import models
from core.models import ACCESSIBILITY_TYPES
from authors.models import Author


class Image(models.Model):
    author = models.ForeignKey(Author, related_name="author")
    url = models.CharField(max_length=256)
    visibility = models.CharField( max_length=128, choices=ACCESSIBILITY_TYPES )
    image = models.ImageField( blank=True, upload_to="Images")

    def __unicode__(self):
        return self.url

    @property
    def base64( self ):
        try:
            img = open( self.image.path, "rb")
            data = img.read()
            return  "data:image/jpg;base64,%s" % data.encode('base64')
        except IOError as e:
            return "error"