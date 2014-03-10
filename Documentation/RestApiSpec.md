Rest API Specification
=========

All of the REST API URIs will begin with the following:
```
hostname/api/
```

Authors
-----------
URI Specification:
```
hostname/api/authors
```
* GET: Returns the JSON representation of all authors on the server.
* POST: Creates a new Author with the specified JSON representation
* PUT: Not Supported
* DELETE: Not Supported

Specific Author
-----------
URI Specification:
```
hostname/api/authors/author_name
```
* GET: Returns the JSON representation of the specific Author.
* POST: Updates the Author with the specified JSON representation
* PUT: Not Supported
* DELETE: If the request has the correct authorization, the specified Author is deleted.

Author's Posts
----------
URI Specification:
```
hostname/api/authors/author_name/posts
```

* GET: Returns the JSON representation of all the posts from the specific Author.
* POST: Creates a new post with the specified JSON representation
* PUT: Not Supported
* DELETE: If the request has the correct authorization, all posts from the Author are deleted.

Author's Specific Post
----------
URI Specification:
```
hostname/api/authors/author_name/posts/post_id
```

* GET: Returns the JSON representation of the specific post from the specific Author.
* POST: Updates the specified post with the specified JSON representation
* PUT: Not Supported
* DELETE: If the request has the correct authorization, the specific post is deleted.

Author's Images
------------
URI Specification:
```
hostname/api/authors/author_name/images
```

* GET: Returns the JSON representation of all the images from the specific Author.
* POST: Creates a new image with the specified JSON representation
* PUT: Not Supported
* DELETE: If the request has the correct authorization, all images from the Author are deleted.


Author's Specific Image
------------
URI Specification:
```
hostname/api/authors/author_name/images/image_id
```

* GET: Returns the JSON representation of the specific image from the specific Author.
* POST: Updates the specified image with the specified JSON representation
* PUT: Not Supported
* DELETE: If the request has the correct authorization, the specific image is deleted.


Author's Friends
------------
URI Specification:
```
hostname/api/authors/author_name/friends
```

* GET: Returns the JSON representation of all the friends from the specific Author.
* POST: Add a new friend to the specified author with the specified JSON friend representation
* PUT: Not Supported
* DELETE: If the request has the correct authorization, all friends from the Author are deleted.


Author's Specific Friend
-------------
URI Specification:
```
hostname/api/authors/author_name/friends/friend_name
```

* GET: Returns the JSON representation of the specific friend from the specific Author.
* POST: Updates the specified friend with the specified JSON representation
* PUT: Not Supported
* DELETE: If the request has the correct authorization, the specific friend is unfriended.