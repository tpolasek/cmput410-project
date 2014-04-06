from django.db import models
from authors.models import Author
from django_extensions.db.fields import UUIDField

#This is a finalized friend object
class Friend(models.Model):
    author = models.ForeignKey(Author, related_name='friends')

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