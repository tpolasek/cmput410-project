from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from social.models import Post, Author, Image, Friend
from django.contrib.auth.models import User

# Create your views here.

def index( request ):
    context = RequestContext( request )
    return render_to_response('social/index.html',{},context)

def get_all_authors(request):
    context = RequestContext( request )

    #Get all authors
    a = Author.objects.all()
    context_dict  = {'authors': a}
    return render_to_response('social/authors.html', context_dict, context )

#get specific author information
def get_author(request, author_name = None):
    context = RequestContext( request )

     #get User object then find the Author object from it
    u = User.objects.get(username__icontains=author_name)
    a = Author.objects.get(user=u)

    #Get all authors
    return render_to_response('social/authors.html', {'author': a}, context )

def get_author_images(request, author_name, image_id = None ):
    context = RequestContext( request )
    
    #get User object then find the Author object from it
    u = User.objects.get(username__icontains=author_name)
    a = Author.objects.get(user=u)
    context_dict = {}
    
    if image_id is not None:
        try:
            context_dict['image'] = Image.objects.get(id=image_id)
        except ObjectDoesNotExist:
            pass #do nothing for now
        
        return render_to_response('social/images.html', context_dict, context )

    context_dict['user_images'] = Image.objects.filter(author=a)
    
    #no content
    return render_to_response('social/images.html', context_dict, context )

def get_author_posts(request, author_name, post_id = None ):
    context = RequestContext( request )

    #get User object then find the Author object from it
    u = User.objects.get(username__icontains=author_name)
    a = Author.objects.get(user=u)
    context_dict = {}

    if post_id is not None:
        try:
            post = Post.objects.get(id=post_id)
            context_dict['post']= post
        except ObjectDoesNotExist:
            pass #do nothing for now

        return render_to_response('social/authors.html', context_dict, context )

    posts = Post.objects.filter(author=a)
    context_dict['user_posts'] = posts

    #no content
    return render_to_response('social/authors.html', context_dict, context )

def get_author_friends(request, author_name, friend_name = None):
    context = RequestContext( request )

    u = User.objects.get(username__icontains=author_name)
    a = Author.objects.get(user=u)
    context_dict = {}

    if friend_name is not None:
        try:
            friend = Friend.objects.get(name=friend_name)
            context_dict['friend'] = friend
        except ObjectDoesNotExist:
            pass # Do nothing for now

        return render_to_response('social/friends.html', context_dict, context )

    friend = Friend.objects.filter(author=a)
    context_dict['user_friends'] = friend

    #no content
    return render_to_response('social/friends.html', context_dict, context )


def register(request):
    context = RequestContext(request)
    return render_to_response('social/register.html', {}, context)

def login(request):
    context = RequestContext(request)
    return render_to_response('social/login.html', {}, context)