from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django_extensions.db.fields import UUIDField
from time import strftime

ACCESSIBILITY_TYPES = (
    ('PUBLIC', 'Public'),
    ('PRIVATE', 'Private'),
    ('private_to_another', 'Private To another author'),
    ('SERVERONLY', 'Friends on this host'),
    ('FRIENDS', 'Friends'),
    ('FOAF', 'Friends of friends'),
)

class Author(models.Model):

    #User already contains: username, password, first_name, last_name, email
    user = models.OneToOneField(User)

    image = models.ImageField( blank=True, upload_to="Images")
    host = models.URLField(max_length=256) #This specifies the authors host

    guid = UUIDField()

    def __unicode__(self):
        return self.user.username

    def json(self):
        return dict (
            id = self.guid,
            host = self.host,
            displayname = self.user.first_name,
        )

    def get_full_name(self):
        return "%s %s" % ( self.user.first_name, self.user.last_name )

#This is a finalized friend object
class Friend(models.Model):
    author = models.ForeignKey(Author)

    friend_name = models.CharField(max_length=256)
    host = models.URLField(max_length=256)

    friend_guid = models.CharField(max_length=256) #This is who is requesting friendship

    url = models.URLField(max_length=256) #This is the url to the friends profile page

    def __unicode__(self):
        return self.friend_name


#This is a friend request that is pending.
#Once the author accepts/denies this request, this will be deleted
#and either used to create a real final friend object or removed if 
#the request was denied
class FriendRequest(models.Model):

    #a friend request is associated with an author
    #and an author can have many friend requests
    author = models.ForeignKey(Author)

    friend_name = models.CharField(max_length=256)
    host = models.URLField(max_length=256)

    friend_guid = UUIDField()   #This is who is requesting friendship
    author_guid = UUIDField()   #This is who he/she is trying to be friends with

    url = models.URLField(max_length=256) #This is the url to the friends profile page


    def __unicode__(self):
        return self.name


class Image(models.Model):
    author = models.ForeignKey(Author, related_name="author")
    url = models.CharField(max_length=256)
    visibility = models.CharField( max_length=128, choices=ACCESSIBILITY_TYPES )

    def __unicode__(self):
        return self.url

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

    def json(self):
        return dict(
            title=self.title,
            source = self.source,
            origin = self.origin,
            description = self.description,
            content_type = self.content_type,
            content=self.content,
            author = self.author.json(),
            categories = [],
            pubDate=self.pubDate.strftime("%a %B %d %c"),
            guid=self.guid,
            visibility=self.visibility,
        )

class Comment(models.Model):
    author = models.ForeignKey(Author)
    pubDate = models.DateTimeField(default=datetime.now)
    post = models.ForeignKey(Post)
    comment = models.TextField()

    guid = UUIDField()

    def __unicode__(self):
        return "%s posted a comment to Post %d" % ( self.author.user.username, self.post.id )

    def json(self):
        return dict(
            author = self.author.json(),
            comment = self.comment,
            pubDate = self.pubDate.strftime("%a %B %d %c"),
            guid = self.guid,
        )