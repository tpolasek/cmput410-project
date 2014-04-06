from rest_framework import serializers
from authors.serializers import AuthorSerializer

from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    url = serializers.URLField(max_length=255)
    visibility = serializers.CharField(max_length=128)
    image = serializers.Field('image.url')

    class Meta:
        model = Image