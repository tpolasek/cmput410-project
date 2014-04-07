from rest_framework import serializers
from .models import Friend, FriendRequest
from authors.serializers import AuthorSerializer

class FriendSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    friend_name = serializers.CharField(max_length=256)
    host = serializers.URLField(max_length=256)

    friend_guid = serializers.CharField(max_length=256)

    url = serializers.URLField(max_length=256)

    class Meta:
        model = Friend

class FriendRequestSerializer(serializers.ModelSerializer):
    
    source_guid = serializers.CharField(max_length=128, source='friend_guid')
    dest_guid = serializers.Field(source='get_author_guid')
    displayname = serializers.CharField(max_length=128,source='friend_name')
    host = serializers.CharField(max_length=128)
    
    url = serializers.URLField(max_length=256)

    class Meta:
        model = FriendRequest
        fields = ['source_guid','dest_guid','displayname','host','url']