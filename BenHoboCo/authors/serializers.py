from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='guid')
    displayname = serializers.Field(source='user.username')
    image = serializers.Field(source="image_url")

    url = serializers.URLField(source="host",max_length=256)
    guid = serializers.CharField(max_length=256)
    github = serializers.CharField(max_length=30)

    class Meta:
        model = Author
        fields = ['id','host','displayname','url' ]