from django.db import models
from django.contrib.auth.models import User

ACCESSIBILITY_TYPES = (
	('public', 'Public'),
	('private', 'Private'),
	('private_to_another', 'Private To another author'),
	('local_friends', 'Friends on this host'),
	('global_friends', 'Friends'),
	('friends_of_friends', 'Friends of friends'),
)

class Author(models.Model):
	user = models.OneToOneField(User)
	image = models.ImageField( blank=True, upload_to="Images")

	def __unicode__(self):
		return self.user.username


class Friend(models.Model):
	name = models.CharField( max_length=32 )
	location = models.URLField()
	author = models.ForeignKey(Author)

	def __unicode__(self):
		return self.name

class Image(models.Model):
	author = models.ForeignKey(Author, related_name="author")
	url = models.CharField(max_length=256)
	accessibility = models.CharField( max_length=128, choices=ACCESSIBILITY_TYPES )

	def __unicode__(self):
		return self.url

class Post(models.Model):
	author = models.ForeignKey(Author)
	time_stamp = models.DateTimeField()
	accessibility = models.CharField( max_length=128, choices=ACCESSIBILITY_TYPES )
	content = models.TextField()

	def __unicode__(self):
		return "%s, %i" % (self.author.user.username, self.id)
