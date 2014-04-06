from django.forms import widgets
from rest_framework import serializers
from .models import Post, Comment
from core.models import ACCESSIBILITY_TYPES
from authors.serializers import AuthorSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    pubDate = serializers.DateTimeField()
    comment = serializers.CharField(widget=widgets.Textarea, max_length=100000)
    guid = serializers.CharField(max_length=256)

    class Meta:
        model = Comment
        fields = ['author','comment','pubDate','guid']

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=256)
    source = serializers.URLField(max_length=256)
    origin = serializers.URLField(max_length=256)

    description = serializers.CharField(widget=widgets.Textarea, max_length=100000)

    content_type = serializers.CharField(max_length=256)
    content = serializers.CharField(widget=widgets.Textarea, max_length=100000)

    categories = serializers.CharField(widget = widgets.Textarea, max_length=100000)

    pubDate = serializers.DateTimeField()

    visibility = serializers.ChoiceField(choices=ACCESSIBILITY_TYPES)

    guid = serializers.CharField(max_length=256)

    author = AuthorSerializer()

    comments = CommentSerializer()

    class Meta:
        model = Post
        fields  = ('title','source','origin','description','content_type','content','author','categories','comments','pubDate','guid','visibility')