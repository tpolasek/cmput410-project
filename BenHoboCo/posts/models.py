from django.db import models
from django_extensions.db.fields import UUIDField
from authors.models import Author
from datetime import datetime
from core.models import ACCESSIBILITY_TYPES

class Post(models.Model):
    author = models.ForeignKey(Author)

    title = models.CharField(max_length=256)
    source = models.URLField(max_length=256)
    origin = models.URLField(max_length=256)

    description = models.CharField(max_length=256)
    content_type = models.CharField(max_length=256)
    content = models.TextField()

    #We may want a separate model for this actually
    categories = models.TextField()

    #We find comments through the comment model.
    #No need for a comments field here

    pubDate = models.DateTimeField(default=datetime.now)
    visibility = models.CharField( max_length=128, choices=ACCESSIBILITY_TYPES )

    guid = UUIDField()

    def __unicode__(self):
        return "%s, %i" % (self.author.user.username, self.id)

class Comment(models.Model):
    author = models.ForeignKey(Author)
    pubDate = models.DateTimeField(default=datetime.now)
    post = models.ForeignKey(Post, related_name="comments")
    comment = models.TextField()

    guid = UUIDField()

    def __unicode__(self):
        return "%s posted a comment to Post %d" % ( self.author.user.username, self.post.id )
