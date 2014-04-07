from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from authors.models import Author
from friends.models import FriendRequest, Friend

import json
import requests

def search_friend(request):
    context = RequestContext(request)
    context_dict = {}

    context_dict['hosts'] = settings.ALLOWED_HOSTS

    if request.method == "POST":
        name = request.POST["friend_name"]
        host = request.POST["host_name"]

        # Some error checking
        if host == "Select Host":
            context_dict["host_unselected"] = True
            return render_to_response('social/friendSearch.html', context_dict, context)

        # Local host
        if host == settings.ALLOWED_HOSTS[0]:
            authors_json = json.dumps( [ author.json() for author in Author.objects.all() ] )

        # Remote host
        else:
            request = requests.get("http://%s/api/authors" % (host))
            authors_json = request.json()

        # At this point we should have an authors JSON object
        all_authors = json.loads( authors_json )

        selected_authors = []
        for author in all_authors:
            if name.lower() in author['displayname'].lower():
                selected_authors.append( { 'name': author['displayname'], 'host': host, 'guid': author['id'] } )

        context_dict['found_authors'] = selected_authors


    return render_to_response('social/friendSearch.html', context_dict, context)

def delete_friend(request, author_guid, friend_guid):
    context = RequestContext( request )

    if request.method == "POST":
        a = Author.objects.get(guid=author_guid)
        u = a.user

        # Is it us trying to delete our own friend?
        if u.username == request.user.username:
            friend = Friend.objects.get(friend_guid=friend_guid, author=a )
            friend.delete()

    return HttpResponseRedirect("/authors/%s/friends/" % a.guid) 

# Accepts a friend request.
def add_friend(request, author_guid):
    context = RequestContext(request)

    try:
        u = User.objects.get(username=author_guid)
        a = Author.objects.get(user=u)
    except User.DoesNotExist:
        a = Author.objects.get(guid=author_guid)
        u = a.user

    context_dict = {'author': a}

    if request.method == "POST":
        new_friend_name = request.POST['friend_name']
        new_friend_guid = request.POST['friend_guid']
        new_friend_location = request.POST['friend_location']

        # If it is blank, it will be localhost
        if not new_friend_location:
            new_friend_location = settings.ALLOWED_HOSTS[0]

        # Integrity check, are they trying to give us an invalid host?
        if new_friend_location in settings.ALLOWED_HOSTS:

            if not Friend.objects.filter(author=a, friend_guid=new_friend_guid):

                # Try aren't a friend already
                print "Not a friend already!"
                # Send the friend request
                if( new_friend_location == settings.ALLOWED_HOSTS[0] ): # Local
                    friended_author = Author.objects.get( guid=new_friend_guid )
                    
                    new_friend_request = FriendRequest( author=a, friend_name=friended_author.get_full_name(), host=friended_author.host, friend_guid=friended_author.guid, author_guid=friended_author.guid )
                    new_friend_request.save()
                else: #Remote
                    remote_author_json = { "author": { "id": new_friend_guid, "host": new_friend_location, "displayname": new_friend_name }, "friend": a.json() }
                    r = requests.post("%s/api/friendrequest"%(new_friend_location), data=remote_author_json)
                    print "Remote friend request reponse code: %s" % (r.status_code)

            if request.user.is_authenticated():
                friendingAuthor = Author.objects.get(guid = new_friend_guid)
                new_friend = Friend(friend_name=a.get_full_name(), host=settings.ALLOWED_HOSTS[0], friend_guid=a.guid, author=friendingAuthor)
                new_friend.save()

    return HttpResponseRedirect('/friends/')

@login_required
def friends(request, friend_id = None):
    context = RequestContext( request )
    context_dict = {}
    user = request.user
    context_dict['user'] = user

    if friend_id is not None:
        f = Friend.objects.get(id = friend_id)
        context_dict['user_friend'] = f
        return render_to_response('social/friend.html', context_dict, context)
    else:
        a = Author.objects.get(user = user)
        f = Friend.objects.filter(author = a)
        friend_requests = FriendRequest.objects.filter(author = a)
        if not f:
            context_dict['user_friends'] = None
        else:
            context_dict['user_friends'] = f
        if friend_requests:
            context_dict['friend_requests'] = friend_requests

    return render_to_response('social/friends.html', context_dict, context)


def get_author_friends(request, author_guid, friend_guid = None):
    context = RequestContext( request )

    a = Author.objects.get(guid=author_guid)
    u = a.user
    context_dict = {}

    if friend_guid is not None:
        try:
            friend = Friend.objects.get(friend_guid=friend_guid, author=a)
            context_dict['friend'] = friend
        except ObjectDoesNotExist:
            pass # Do nothing for now

        return render_to_response('social/friends.html', context_dict, context )

    friend = Friend.objects.filter(author=a)
    context_dict['user_friends'] = friend
    context_dict['author'] = a

    #no content
    return render_to_response('social/friends.html', context_dict, context )

@login_required
def accept_friend_request(request, friend_id):
    context = RequestContext(request)
    a = Author.objects.get(user = request.user)
    context_dict = {}

    friendRequest = FriendRequest.objects.get(author = a, friend_guid = friend_id)
    if friendRequest is not None:
        new_friend = Friend(friend_name=friendRequest.friend_name, host=friendRequest.host, friend_guid=friendRequest.friend_guid, author=a)
        new_friend.save()
        friendRequest.delete()

    return HttpResponseRedirect('/friends')
