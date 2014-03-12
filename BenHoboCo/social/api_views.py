from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from social.forms import UserForm, AuthorForm, ImageUploadForm
from django.db.models import Q

from social.models import Post, Author, Image, Friend, Comment
from django.contrib.auth.models import User
from django.core import serializers
from django.forms.models import model_to_dict

import json

# Create your views here.

def get_authors(request, author_guid=None):

    if author_guid is not None:
        a = {Author.objects.get(guid=author_guid)}
    else:
        a = Author.objects.all()

    #return HttpResponse( serializers.serialize( 'json', a ) )

    if request.method == "POST":
        #Implement the creation of author with json data
        pass

    data = [ author.json() for author in a ]
    return HttpResponse( json.dumps(data), content_type="application/json")

def get_posts(request, author_guid = None, post_guid = None ):

    if author_guid is not None:
        try:
            author = Author.objects.get(guid=author_guid)

            if post_guid is not None:
                posts = {Post.objects.get(guid=post_guid)}
            else:
                posts = Post.objects.filter(author=author)

            data = [ post.json() for post in posts ]

            for d in data:
                pguid = d['guid']
                post = Post.objects.get(guid=pguid)
                comments = Comment.objects.filter(post=post)
                d['comments'] = [ c.json() for c in comments ]

            return HttpResponse( json.dumps(data), content_type="application/json")
        except ObjectDoesNotExist:
            print "Cannot find user"
            pass