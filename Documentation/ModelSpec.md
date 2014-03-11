Model Specification
=========

Post
----------

* (Text) Title
* (Text/ URL) Source
* (Text / URL) Origin
* (Text) Description
* (Text) Content-Type
* (Text) Content
* (List of Text) Categories
* (Author Object) Author
* (List of Comment Objects) Comments
* (DateTime) Time_stamp
* (GUID) Post ID
* (Visibility Type) Visibility

Comment
---------

* (Author Object) Author
* (Text) Comment Text
* (DateTime) Time_stamp
* (GUID) Comment ID

Author
----------
* (GUID) Author ID
* (Text) Author Name
* (Text/URL) Author Host

FriendObject
----------
* (Author Object) Author
* (Text) Friend Name
* (Text/URL) Friend Host
* (GUID) Friend ID
* (Text/URL) Friend URL (to profile page)

FriendRequest
----------
* (Text) Friend Name
* (Text/URL) Friend Host
* (GUID) Friend ID
* (Text/URL) Friend URL (to profile page)
* (GUID) TargetAuthor ID