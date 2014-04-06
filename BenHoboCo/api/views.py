from rest_framework import generics, permissions
from rest_framework.views import APIView

from authors.serializers import AuthorSerializer
from friends.serializers import FriendSerializer, FriendRequestSerializer
from images.serializers import ImageSerializer
from posts.serializers import PostSerializer

from authors.models import Author
from friends.models import Friend
from images.models import Image
from posts.models import Post

from rest_framework.response import Response

##AUTHOR SECTION
# GET: Returns the JSON representation of all authors on the server.
# POST: Creates a new Author with the specified JSON representation
# PUT: Not Supported
# DELETE: Not Supported
class AuthorList(generics.ListCreateAPIView):
    model = Author
    serializer_class = AuthorSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

# GET: Returns the JSON representation of the specific Author.
# POST: Updates the Author with the specified JSON representation
# PUT: Not Supported
# DELETE: If the request has the correct authorization, the specified Author is deleted.
class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Author
    serializer_class = AuthorSerializer
    lookup_field = 'guid'
    permissions_classes = [
        permissions.AllowAny
    ]

##FRIENDS SECTION
# GET: Returns the JSON representation of all the friends from the specific Author.
# POST: Add a new friend to the specified author with the specified JSON friend representation
# PUT: Not Supported
# DELETE: If the request has the correct authorization, all friends from the Author are deleted.
class FriendList(generics.ListCreateAPIView):
    model = Friend
    serializer_class = FriendSerializer

    def get_queryset(self):
        queryset = super(FriendList, self).get_queryset()
        author = self.request.user.author
        return queryset.filter(author = author )

# GET: Returns the JSON representation of the specific friend from the specific Author.
# POST: Updates the specified friend with the specified JSON representation
# PUT: Update the specified friend with the specified JSON representation
# DELETE: If the request has the correct authorization, the specific friend is unfriended.
class FriendDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Friend
    serializer_class = AuthorSerializer

    permissions_classes = [
        permissions.AllowAny
    ]

class FriendCompare(APIView):

    def get(self, request, *args, **kwargs):
        guid_1 = kwargs['guid_1']
        guid_2 = kwargs['guid_2']

        dict = { 'query':'friends', 'comparing': [ guid_1, guid_2 ], 'friends':'YES'}
        ##TODO Insert function here to compare the guids and check if they're friends

        return Response(dict)

class FriendRequest(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FriendRequestSerializer(data=request.DATA)

        dict = {}

        return Response(dict)


##IMAGE SECTION
class ImageList(generics.ListCreateAPIView):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        queryset = super(ImageList,self).get_queryset()
        author = self.request.user.author
        return queryset.filter(author = author )

class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Image
    serializer_class = ImageSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

##POST SECTION
# GET: Returns the list of all public posts on our server
# POST: Adds a new post
class PostList(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        queryset = super(PostList,self).get_queryset()
        # from here we will retrieve all "PUBLIC" Posts
        return queryset.filter(visibility = "PUBLIC" )

class AuthorPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super(AuthorPostList,self).get_queryset()
        # Get all the posts for that user
        # that is visible to the authenticated user
        #  TODO: make this for the authenticated user
        #  Just need to add another filter for the visibility
        #  after we add authentication for the user
        # author = self.request.user.author
        author = Author.objects.get(guid=self.kwargs.get('guid'))
        return queryset.filter( author = author )

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    serializer_class = PostSerializer
    permissions_classes = [
        permissions.AllowAny
    ]
    lookup_field = 'guid'

