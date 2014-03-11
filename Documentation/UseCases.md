Use Cases
============


1.  Seeing Friend of Friend Posts
----------------------

1. Login
2. Find Friend of Friend
3. Click Link to Friend of Friend
4. Server sends a REST API call to get all accessible posts
5. Server renders an HTML Page with the friend of friend posts


2.  Friending Someone
---------------------

1. I get a friend request through REST API
	1b. The host of the requester creates a "Friend Object" that they implement to record the friend relationship
2. My host creates a friend request object
3. When I log in, I see the friend request
4. If I accept the friend request:
	4a. My host creates a friend object
	4b. The friend request object is deleted.
5. If I reject the friend request:
	5a. The friend request is deleted.
	5b. (maybe send a response back saying we rejected?)
